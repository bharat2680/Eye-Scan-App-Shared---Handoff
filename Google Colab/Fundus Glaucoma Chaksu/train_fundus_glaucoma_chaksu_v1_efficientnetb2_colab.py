from __future__ import annotations

import hashlib
import json
import random
import re
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import tensorflow as tf


SEED = 42
RUN_NAME = "fundus_glaucoma_chaksu_v1_efficientnetb2_colab"
CLASS_NAMES = ["Healthy", "Glaucoma"]
IMAGE_SIZE = (260, 260)
BATCH_SIZE = 12
FROZEN_EPOCHS = 5
FINETUNE_EPOCHS = 10
EARLY_STOPPING_PATIENCE = 3
VAL_PERCENT = 20
PARTIAL_UNFREEZE_LAYERS = 120
FIGSHARE_ARTICLE_ID = 20123135
FIGSHARE_FALLBACK_DIR = Path("/content/figshare_downloads")


def seed_everything() -> None:
    random.seed(SEED)
    np.random.seed(SEED)
    tf.random.set_seed(SEED)
    try:
        tf.keras.utils.set_random_seed(SEED)
        tf.config.experimental.enable_op_determinism()
    except Exception:
        pass


def enable_mixed_precision_if_gpu() -> None:
    if tf.config.list_physical_devices("GPU"):
        try:
            tf.keras.mixed_precision.set_global_policy("mixed_float16")
        except Exception:
            pass


def import_pandas():
    try:
        import pandas as pd
    except ImportError:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", "pandas", "openpyxl"],
            check=True,
        )
        import pandas as pd
    return pd


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _sanitize_keras_archive(model_path: Path) -> None:
    tmp_path = model_path.with_suffix(model_path.suffix + ".tmp")
    with zipfile.ZipFile(model_path) as src:
        config = json.loads(src.read("config.json"))
        metadata = src.read("metadata.json")
        weights = src.read("model.weights.h5")

    def strip_quantization(obj):
        if isinstance(obj, dict):
            obj.pop("quantization_config", None)
            for value in obj.values():
                strip_quantization(value)
        elif isinstance(obj, list):
            for value in obj:
                strip_quantization(value)

    strip_quantization(config)
    with zipfile.ZipFile(tmp_path, "w", compression=zipfile.ZIP_DEFLATED) as dst:
        dst.writestr("metadata.json", metadata)
        dst.writestr("config.json", json.dumps(config))
        dst.writestr("model.weights.h5", weights)
    tmp_path.replace(model_path)


def _drive_zip_candidates(datasets_root: Path) -> list[Path]:
    return [
        datasets_root / "Chaksu.zip",
        datasets_root / "chaksu.zip",
        datasets_root / "Chakshu.zip",
        datasets_root / "Chaksu_IMAGE.zip",
        datasets_root / "Chaksu_IMAGE_v2.zip",
    ]


def _find_existing_raw_zip(datasets_root: Path) -> Path | None:
    for candidate in _drive_zip_candidates(datasets_root):
        if candidate.exists():
            return candidate
    return None


def _download_with_progress(url: str, target_path: Path) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)

    def _report(blocks: int, block_size: int, total_size: int) -> None:
        if total_size <= 0:
            return
        downloaded = min(blocks * block_size, total_size)
        percent = (downloaded / total_size) * 100
        print(f"\rDownloading {target_path.name}: {percent:5.1f}% ({downloaded}/{total_size} bytes)", end="")

    urllib.request.urlretrieve(url, target_path, reporthook=_report)
    print()


def _download_latest_figshare_chaksu() -> tuple[Path, dict]:
    article_api = f"https://api.figshare.com/v2/articles/{FIGSHARE_ARTICLE_ID}"
    with urllib.request.urlopen(article_api) as response:
        article = json.loads(response.read().decode("utf-8"))

    files = article.get("files", [])
    if not files:
        raise RuntimeError(f"No downloadable files found in Figshare article {FIGSHARE_ARTICLE_ID}")

    chosen = None
    for file_info in files:
        name = str(file_info.get("name", ""))
        if name.lower().endswith(".zip") and ("ch" in name.lower() or "image" in name.lower()):
            chosen = file_info
            break
    if chosen is None:
        zip_files = [file_info for file_info in files if str(file_info.get("name", "")).lower().endswith(".zip")]
        if zip_files:
            chosen = max(zip_files, key=lambda file_info: int(file_info.get("size", 0) or 0))
    if chosen is None:
        chosen = files[0]

    version = article.get("version", "latest")
    download_url = chosen.get("download_url")
    if not download_url:
        raise RuntimeError(f"Figshare file metadata did not include download_url: {chosen}")

    suffix = Path(str(chosen.get("name", "Chaksu.zip"))).suffix or ".zip"
    target_path = FIGSHARE_FALLBACK_DIR / f"Chaksu_figshare_v{version}{suffix}"
    if not target_path.exists():
        print(f"Downloading Chaksu from Figshare version {version} to: {target_path}")
        _download_with_progress(download_url, target_path)
    else:
        print(f"Reusing existing Figshare download: {target_path}")

    source_info = {
        "source_kind": "figshare_public_download",
        "article_id": FIGSHARE_ARTICLE_ID,
        "version": version,
        "article_url": article.get("url_public_html") or f"https://figshare.com/articles/dataset/{FIGSHARE_ARTICLE_ID}",
        "file_name": chosen.get("name"),
        "download_url": download_url,
    }
    return target_path, source_info


def _bucket_for_name(name: str) -> int:
    digest = hashlib.sha1(name.encode("utf-8")).hexdigest()
    return int(digest, 16) % 100


def _is_validation_member(image_id: str) -> bool:
    return _bucket_for_name(image_id) < VAL_PERCENT


def _normalize_token(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def _normalize_image_key(value: object) -> str:
    text = str(value).strip()
    if not text:
        return ""
    name = Path(text).name
    stem = Path(name).stem
    return _normalize_token(stem)


def _load_table(path: Path):
    pd = import_pandas()
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    return None


def _find_image_col(frame) -> str | None:
    candidate_columns = list(frame.columns)
    scored: list[tuple[int, str]] = []
    for column in candidate_columns:
        normalized = _normalize_token(str(column))
        series = frame[column].astype(str)
        sample = " ".join(series.head(10).tolist()).lower()
        score = 0
        if any(token in normalized for token in ["image", "filename", "fundus", "file", "name", "img"]):
            score += 3
        if any(ext in sample for ext in [".jpg", ".jpeg", ".png", ".bmp"]):
            score += 4
        if score:
            scored.append((score, column))
    if scored:
        scored.sort(reverse=True)
        return scored[0][1]
    if len(candidate_columns) > 0:
        return candidate_columns[0]
    return None


def _parse_binary_label(value: object) -> int | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none"}:
        return None
    lowered = text.lower()
    if "glau" in lowered and "non" not in lowered and "normal" not in lowered:
        return 1
    if any(token in lowered for token in ["normal", "healthy", "nonglau", "non-glau"]):
        return 0
    try:
        number = float(text)
    except Exception:
        return None
    if number in {0.0, 1.0}:
        return int(number)
    return None


def _extract_decisions_from_tables(decision_root: Path) -> tuple[dict[str, int], dict]:
    table_paths = sorted(
        [
            path
            for path in decision_root.rglob("*")
            if path.is_file() and path.suffix.lower() in {".csv", ".xlsx", ".xls"}
        ]
    )
    direct_labels: dict[str, int] = {}
    votes: dict[str, list[int]] = {}
    debug_tables: list[dict[str, object]] = []
    conflicts = 0

    for table_path in table_paths:
        frame = _load_table(table_path)
        if frame is None or frame.empty:
            continue
        frame = frame.copy()
        frame.columns = [str(column).strip() for column in frame.columns]
        image_col = _find_image_col(frame)
        if image_col is None:
            continue

        normalized_columns = {_normalize_token(str(column)): str(column) for column in frame.columns}
        direct_cols = [
            column
            for column in frame.columns
            if any(token in _normalize_token(str(column)) for token in ["majority", "final", "decision", "label", "class"])
            and "expert" not in _normalize_token(str(column))
        ]
        expert_cols = [
            column
            for column in frame.columns
            if "expert" in _normalize_token(str(column)) or re.search(r"\b[eE][1-5]\b", str(column))
        ]

        parsed_rows = 0
        direct_hits = 0
        vote_hits = 0
        for row in frame.itertuples(index=False, name=None):
            row_dict = dict(zip(frame.columns, row))
            key = _normalize_image_key(row_dict.get(image_col))
            if not key:
                continue
            parsed_rows += 1

            direct_label = None
            for column in direct_cols:
                direct_label = _parse_binary_label(row_dict.get(column))
                if direct_label is not None:
                    break
            if direct_label is not None:
                direct_hits += 1
                if key in direct_labels and direct_labels[key] != direct_label:
                    conflicts += 1
                direct_labels[key] = direct_label

            row_votes = [_parse_binary_label(row_dict.get(column)) for column in expert_cols]
            row_votes = [vote for vote in row_votes if vote is not None]
            if row_votes:
                vote_hits += len(row_votes)
                votes.setdefault(key, []).extend(row_votes)

        debug_tables.append(
            {
                "path": str(table_path.relative_to(decision_root)),
                "rows": int(parsed_rows),
                "direct_label_columns": direct_cols,
                "expert_columns": expert_cols,
                "direct_hits": direct_hits,
                "vote_hits": vote_hits,
            }
        )

    decisions = dict(direct_labels)
    majority_from_votes = 0
    for key, key_votes in votes.items():
        if key in decisions or not key_votes:
            continue
        decisions[key] = 1 if sum(key_votes) >= (len(key_votes) / 2.0) else 0
        majority_from_votes += 1

    debug = {
        "table_count": len(table_paths),
        "tables": debug_tables[:20],
        "direct_label_count": len(direct_labels),
        "majority_from_votes_count": majority_from_votes,
        "conflicts": conflicts,
    }
    return decisions, debug


def _extract_chaksu_dataset(
    raw_zip: Path,
    raw_extract_root: Path,
    dataset_root: Path,
) -> tuple[dict[str, dict[str, int]], dict]:
    if raw_extract_root.exists():
        shutil.rmtree(raw_extract_root)
    if dataset_root.exists():
        shutil.rmtree(dataset_root)
    raw_extract_root.mkdir(parents=True, exist_ok=True)
    dataset_root.mkdir(parents=True, exist_ok=True)

    keep_table_suffixes = {".csv", ".xlsx", ".xls"}
    keep_image_suffixes = {".jpg", ".jpeg", ".png", ".bmp"}

    with zipfile.ZipFile(raw_zip) as archive:
        for member in archive.infolist():
            if member.is_dir():
                continue
            name = member.filename
            lowered = name.lower()
            suffix = Path(name).suffix.lower()
            keep = False
            if "1.0_original_fundus_images" in lowered and suffix in keep_image_suffixes:
                keep = True
            elif "glaucoma" in lowered and "decision" in lowered and suffix in keep_table_suffixes:
                keep = True
            if keep:
                archive.extract(member, raw_extract_root)

    image_files = sorted(
        [
            path
            for path in raw_extract_root.rglob("*")
            if path.is_file() and path.suffix.lower() in keep_image_suffixes and "1.0_original_fundus_images" in str(path).lower()
        ]
    )
    if not image_files:
        raise RuntimeError("No Chaksu original fundus images were extracted from the archive")

    image_map: dict[str, Path] = {}
    image_split_lookup: dict[str, str] = {}
    device_counts = {"train": {}, "test": {}}
    split_image_counts = {"train_total_images": 0, "test_total_images": 0}
    for image_path in image_files:
        relative = image_path.relative_to(raw_extract_root)
        parts = [part for part in relative.parts]
        lowered_parts = [part.lower() for part in parts]
        split_name = "train" if any("train" in part for part in lowered_parts) else "test"
        device_name = parts[-2] if len(parts) >= 2 else "unknown"
        device_counts[split_name][device_name] = device_counts[split_name].get(device_name, 0) + 1
        split_image_counts[f"{split_name}_total_images"] += 1
        key = _normalize_image_key(image_path.name)
        image_map[key] = image_path
        image_split_lookup[key] = split_name

    decision_tables = sorted(
        [
            path
            for path in raw_extract_root.rglob("*")
            if path.is_file()
            and path.suffix.lower() in keep_table_suffixes
            and "glaucoma" in str(path).lower()
            and "decision" in str(path).lower()
        ]
    )
    if not decision_tables:
        sample_paths = [str(path.relative_to(raw_extract_root)) for path in sorted(raw_extract_root.rglob("*"))[:80]]
        raise RuntimeError(
            "Could not find any glaucoma-decision tables under the extracted Chaksu subset. "
            f"Sample extracted paths: {sample_paths}"
        )

    train_decision_tables = [path for path in decision_tables if "train" in str(path).lower()]
    test_decision_tables = [path for path in decision_tables if "test" in str(path).lower()]
    if train_decision_tables and test_decision_tables:
        train_decisions, train_decision_debug = _extract_decisions_from_tables(train_decision_tables[0].parent)
        test_decisions, test_decision_debug = _extract_decisions_from_tables(test_decision_tables[0].parent)
        split_assignment_mode = "separate_train_and_test_decision_roots"
    else:
        all_decisions, all_decision_debug = _extract_decisions_from_tables(decision_tables[0].parent.parent)
        train_decisions = {}
        test_decisions = {}
        for key, label in all_decisions.items():
            split_name = image_split_lookup.get(key)
            if split_name == "train":
                train_decisions[key] = label
            elif split_name == "test":
                test_decisions[key] = label
        train_decision_debug = all_decision_debug
        test_decision_debug = {
            "mode": "reused_global_decision_tables_via_image_split_lookup",
            "derived_test_labels": len(test_decisions),
        }
        split_assignment_mode = "shared_decision_tables_routed_by_image_split"

    counts = {
        "train": {"Healthy": 0, "Glaucoma": 0},
        "valid": {"Healthy": 0, "Glaucoma": 0},
        "test": {"Healthy": 0, "Glaucoma": 0},
    }

    missing_images = {"train": 0, "test": 0}
    for split_name, decisions in [("train", train_decisions), ("test", test_decisions)]:
        for key, label in decisions.items():
            image_path = image_map.get(key)
            if image_path is None:
                missing_images[split_name] += 1
                continue
            class_name = "Healthy" if label == 0 else "Glaucoma"
            final_split = split_name
            if split_name == "train":
                final_split = "valid" if _is_validation_member(image_path.stem) else "train"
            target_path = dataset_root / final_split / class_name / image_path.name
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(image_path, target_path)
            counts[final_split][class_name] += 1

    debug = {
        **split_image_counts,
        "device_counts": device_counts,
        "decision_table_count": len(decision_tables),
        "decision_split_assignment_mode": split_assignment_mode,
        "train_decision_table_examples": [str(path.relative_to(raw_extract_root)) for path in train_decision_tables[:10]],
        "test_decision_table_examples": [str(path.relative_to(raw_extract_root)) for path in test_decision_tables[:10]],
        "train_decision_debug": train_decision_debug,
        "test_decision_debug": test_decision_debug,
        "missing_images_for_decisions": missing_images,
    }
    if sum(sum(class_counts.values()) for class_counts in counts.values()) == 0:
        raise RuntimeError(f"No Chaksu labeled images were staged. Debug: {debug}")

    return counts, debug


def compute_class_weights(train_counts: dict[str, int]) -> dict[int, float]:
    label_counts = {0: int(train_counts["Healthy"]), 1: int(train_counts["Glaucoma"])}
    total = sum(label_counts.values())
    return {label: total / (2 * max(count, 1)) for label, count in label_counts.items()}


def make_split_dataset(dataset_root: Path, split_name: str, training: bool) -> tf.data.Dataset:
    split_dir = dataset_root / split_name
    dataset = tf.keras.utils.image_dataset_from_directory(
        split_dir,
        labels="inferred",
        label_mode="binary",
        class_names=CLASS_NAMES,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=training,
        seed=SEED,
    )
    return dataset.prefetch(tf.data.AUTOTUNE)


def build_model() -> tuple[tf.keras.Model, tf.keras.Model]:
    augmentation = tf.keras.Sequential(
        [
            tf.keras.layers.RandomFlip("horizontal"),
            tf.keras.layers.RandomRotation(0.03),
            tf.keras.layers.RandomTranslation(0.04, 0.04),
            tf.keras.layers.RandomZoom(0.10),
            tf.keras.layers.RandomContrast(0.10),
        ],
        name="augmentation",
    )
    backbone = tf.keras.applications.EfficientNetB2(
        include_top=False,
        weights="imagenet",
        input_shape=IMAGE_SIZE + (3,),
        pooling="avg",
    )
    backbone.trainable = False

    inputs = tf.keras.Input(shape=IMAGE_SIZE + (3,))
    x = augmentation(inputs)
    x = backbone(x, training=False)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.45)(x)
    outputs = tf.keras.layers.Dense(
        1,
        activation="sigmoid",
        dtype="float32",
        kernel_regularizer=tf.keras.regularizers.l2(1e-4),
    )(x)
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    return model, backbone


def compile_model(model: tf.keras.Model, learning_rate: float) -> None:
    model.compile(
        optimizer=tf.keras.optimizers.AdamW(learning_rate=learning_rate, weight_decay=1e-5),
        loss=tf.keras.losses.BinaryCrossentropy(label_smoothing=0.02),
        metrics=["accuracy", tf.keras.metrics.AUC(name="auc")],
    )


def collect_predictions(model: tf.keras.Model, dataset: tf.data.Dataset) -> tuple[np.ndarray, np.ndarray]:
    probabilities = model.predict(dataset, verbose=0).reshape(-1)
    labels = np.concatenate([batch_labels.numpy().reshape(-1) for _, batch_labels in dataset], axis=0).astype(int)
    return probabilities, labels


def confusion_for_threshold(y_true: np.ndarray, y_prob: np.ndarray, threshold: float) -> list[list[int]]:
    y_pred = (y_prob >= threshold).astype(int)
    tp = int(np.sum((y_true == 1) & (y_pred == 1)))
    tn = int(np.sum((y_true == 0) & (y_pred == 0)))
    fp = int(np.sum((y_true == 0) & (y_pred == 1)))
    fn = int(np.sum((y_true == 1) & (y_pred == 0)))
    return [[tn, fp], [fn, tp]]


def balanced_accuracy_from_confusion(confusion: list[list[int]]) -> float:
    tn, fp = confusion[0]
    fn, tp = confusion[1]
    negative_recall = tn / max(tn + fp, 1)
    positive_recall = tp / max(tp + fn, 1)
    return (negative_recall + positive_recall) / 2.0


def find_best_threshold(y_true: np.ndarray, y_prob: np.ndarray) -> tuple[float, float, list[list[int]]]:
    best_threshold = 0.5
    best_score = -1.0
    best_confusion = [[0, 0], [0, 0]]
    for threshold in np.linspace(0.1, 0.9, 17):
        confusion = confusion_for_threshold(y_true, y_prob, float(threshold))
        score = balanced_accuracy_from_confusion(confusion)
        if score > best_score:
            best_score = score
            best_threshold = float(round(threshold, 2))
            best_confusion = confusion
    return best_threshold, best_score, best_confusion


def round_history(history: tf.keras.callbacks.History) -> dict[str, list[float]]:
    return {key: [round(float(value), 6) for value in values] for key, values in history.history.items()}


def _set_trainable_range(backbone: tf.keras.Model, unfreeze_layers: int) -> None:
    backbone.trainable = True
    trainable_start = max(len(backbone.layers) - unfreeze_layers, 0)
    for index, layer in enumerate(backbone.layers):
        keep_frozen = index < trainable_start or isinstance(layer, tf.keras.layers.BatchNormalization)
        layer.trainable = not keep_frozen


def main() -> None:
    from google.colab import drive

    drive.mount("/content/drive")
    seed_everything()
    enable_mixed_precision_if_gpu()

    drive_root = Path("/content/drive/MyDrive")
    datasets_root = drive_root / "Datasets"
    workdir = Path("/content/eyescan_chaksu_colab_v1")
    raw_extract_root = workdir / "chaksu_subset"
    dataset_root = workdir / "Chaksu_Glaucoma_vs_Healthy"
    output_dir = drive_root / "EyeScan_Models" / "Fundus_Glaucoma_Chaksu_V1"
    workdir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_zip = _find_existing_raw_zip(datasets_root)
    source_info = None
    if raw_zip is None:
        raw_zip, source_info = _download_latest_figshare_chaksu()
    else:
        source_info = {
            "source_kind": "google_drive_upload",
            "article_id": FIGSHARE_ARTICLE_ID,
            "version": None,
            "article_url": "https://figshare.com/articles/dataset/Ch_k_u_A_glaucoma_specific_fundus_image_database/20123135",
            "file_name": raw_zip.name,
            "download_url": None,
        }

    print("Using raw archive:", raw_zip)
    counts, debug = _extract_chaksu_dataset(raw_zip, raw_extract_root, dataset_root)
    print("Counts:", json.dumps(counts, indent=2))
    print("Dataset debug:", json.dumps(debug, indent=2))

    train_counts = counts["train"]
    class_weights = compute_class_weights(train_counts)

    gpu_devices = tf.config.list_physical_devices("GPU")
    print("TensorFlow version:", tf.__version__)
    print("GPU devices:", gpu_devices)
    print("Mixed precision policy:", tf.keras.mixed_precision.global_policy())
    print("Class weights:", class_weights)

    train_ds = make_split_dataset(dataset_root, "train", training=True)
    val_ds = make_split_dataset(dataset_root, "valid", training=False)
    test_ds = make_split_dataset(dataset_root, "test", training=False)

    best_model_path = output_dir / "best_model.keras"
    model, backbone = build_model()
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_auc",
            mode="max",
            patience=EARLY_STOPPING_PATIENCE,
            restore_best_weights=True,
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_auc",
            mode="max",
            factor=0.5,
            patience=2,
            min_lr=1e-7,
            verbose=1,
        ),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=best_model_path,
            monitor="val_auc",
            mode="max",
            save_best_only=True,
        ),
    ]

    compile_model(model, learning_rate=3e-4)
    history_frozen = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=FROZEN_EPOCHS,
        callbacks=callbacks,
        class_weight=class_weights,
        verbose=2,
    )

    _set_trainable_range(backbone, PARTIAL_UNFREEZE_LAYERS)
    compile_model(model, learning_rate=3e-5)
    history_finetune = model.fit(
        train_ds,
        validation_data=val_ds,
        initial_epoch=len(history_frozen.history["loss"]),
        epochs=FROZEN_EPOCHS + FINETUNE_EPOCHS,
        callbacks=callbacks,
        class_weight=class_weights,
        verbose=2,
    )

    _sanitize_keras_archive(best_model_path)
    model = tf.keras.models.load_model(best_model_path, compile=False)

    val_prob, val_true = collect_predictions(model, val_ds)
    test_prob, test_true = collect_predictions(model, test_ds)
    selected_threshold, val_bal_acc, val_confusion = find_best_threshold(val_true, val_prob)
    default_test_confusion = confusion_for_threshold(test_true, test_prob, 0.5)
    tuned_test_confusion = confusion_for_threshold(test_true, test_prob, selected_threshold)

    metrics = {
        "run_name": RUN_NAME,
        "dataset_root": str(dataset_root),
        "output_dir": str(output_dir),
        "image_size": list(IMAGE_SIZE),
        "batch_size": BATCH_SIZE,
        "class_names": CLASS_NAMES,
        "counts": counts,
        "class_weights": {str(key): value for key, value in class_weights.items()},
        "official_protocol": {
            "dataset": "Chaksu IMAGE",
            "official_train_test_split": True,
            "official_article_url": "https://www.nature.com/articles/s41597-023-01943-4",
            "official_figshare_url": "https://figshare.com/articles/dataset/Ch_k_u_A_glaucoma_specific_fundus_image_database/20123135",
        },
        "dataset_source": {
            "raw_archive_zip": str(raw_zip),
            **source_info,
        },
        "dataset_debug": debug,
        "device": {"gpu_count": len(gpu_devices), "gpu_names": [device.name for device in gpu_devices]},
        "history": {
            "frozen": round_history(history_frozen),
            "finetune": round_history(history_finetune),
        },
        "validation": {
            "selected_threshold": selected_threshold,
            "balanced_accuracy": val_bal_acc,
            "confusion_matrix": val_confusion,
        },
        "test": {
            "default_threshold": {
                "threshold": 0.5,
                "accuracy": float(np.mean((test_prob >= 0.5).astype(int) == test_true)),
                "balanced_accuracy": balanced_accuracy_from_confusion(default_test_confusion),
                "confusion_matrix": default_test_confusion,
            },
            "tuned_threshold": {
                "threshold": selected_threshold,
                "accuracy": float(np.mean((test_prob >= selected_threshold).astype(int) == test_true)),
                "balanced_accuracy": balanced_accuracy_from_confusion(tuned_test_confusion),
                "confusion_matrix": tuned_test_confusion,
            },
        },
    }
    label_map = {"healthy": 0, "glaucoma": 1}
    inference_contract = {
        "run_name": RUN_NAME,
        "model_file": "best_model.keras",
        "labels": ["healthy", "glaucoma"],
        "input": {
            "image_size": list(IMAGE_SIZE),
            "color_mode": "rgb",
            "dtype": "float32",
            "resize_mode": "resize_with_pad",
            "normalization": "efficientnet_pretrained_internal_scaling",
        },
        "decision": {
            "rule": "threshold_on_positive_probability",
            "positive_label": "glaucoma",
            "selected_threshold": selected_threshold,
            "selection_split": "val",
            "selection_objective": "balanced_accuracy",
            "argmax_fallback": True,
        },
        "intended_use": "Evaluation-only glaucoma-vs-healthy screening candidate using the official Chaksu train/test split and majority-vote glaucoma decisions.",
        "deployment_status": "evaluation_only",
    }
    train_history = {
        "frozen": round_history(history_frozen),
        "finetune": round_history(history_finetune),
    }
    train_config = {
        "run_name": RUN_NAME,
        "class_names": CLASS_NAMES,
        "image_size": list(IMAGE_SIZE),
        "batch_size": BATCH_SIZE,
        "frozen_epochs": FROZEN_EPOCHS,
        "finetune_epochs": FINETUNE_EPOCHS,
        "early_stopping_patience": EARLY_STOPPING_PATIENCE,
        "validation_percent_within_official_training_split": VAL_PERCENT,
        "partial_unfreeze_layers": PARTIAL_UNFREEZE_LAYERS,
        "raw_archive_zip": str(raw_zip),
        "output_dir": str(output_dir),
        "model_family": "efficientnetb2_imagenet",
        "class_weighting": class_weights,
        "resize_mode": "resize_with_pad",
        "paper_correction_note": "Author correction published 2023-04-06; current assumption is that the official train/test split and majority-vote glaucoma decision semantics remain unchanged for this image-only recipe.",
        "source_info": source_info,
    }

    write_json(output_dir / "metrics.json", metrics)
    write_json(output_dir / "label_map.json", label_map)
    write_json(output_dir / "inference_contract.json", inference_contract)
    write_json(output_dir / "train_history.json", train_history)
    write_json(output_dir / "train_config.json", train_config)

    print(json.dumps(metrics, indent=2))
    print(f"Saved artifacts to: {output_dir}")


if __name__ == "__main__":
    main()
