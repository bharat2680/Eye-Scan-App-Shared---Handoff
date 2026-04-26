from __future__ import annotations

import hashlib
import json
import math
import random
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import tensorflow as tf


SEED = 42
RUN_NAME = "fundus_glaucoma_papila_v3_efficientnetb2_officialfold_colab"
CLASS_DIRS = ["Healthy", "Glaucoma"]
IMAGE_SIZE = (260, 260)
BATCH_SIZE = 12
FROZEN_EPOCHS = 6
PARTIAL_FINETUNE_EPOCHS = 10
DEEP_FINETUNE_EPOCHS = 8
EARLY_STOPPING_PATIENCE = 4
VAL_PATIENT_PERCENT = 20
PARTIAL_UNFREEZE_LAYERS = 120
DEEP_UNFREEZE_LAYERS = 220
FOLD_INDEX = 1
FIGSHARE_ARTICLE_ID = 14798004
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


def _raw_zip_candidates(datasets_root: Path) -> list[Path]:
    return [
        datasets_root / "PAPILA.zip",
        datasets_root / "Papila.zip",
        datasets_root / "papila.zip",
        datasets_root / "PAPILA_v2.zip",
    ]


def _find_existing_raw_zip(datasets_root: Path) -> Path | None:
    for candidate in _raw_zip_candidates(datasets_root):
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


def _download_latest_figshare_papila() -> tuple[Path, dict]:
    article_api = f"https://api.figshare.com/v2/articles/{FIGSHARE_ARTICLE_ID}"
    with urllib.request.urlopen(article_api) as response:
        article = json.loads(response.read().decode("utf-8"))

    files = article.get("files", [])
    if not files:
        raise RuntimeError(f"No downloadable files found in Figshare article {FIGSHARE_ARTICLE_ID}")

    chosen = None
    for file_info in files:
        name = str(file_info.get("name", ""))
        if name.lower().endswith(".zip") and "papila" in name.lower():
            chosen = file_info
            break
    if chosen is None:
        for file_info in files:
            name = str(file_info.get("name", ""))
            if name.lower().endswith(".zip"):
                chosen = file_info
                break
    if chosen is None:
        chosen = files[0]

    version = article.get("version", "latest")
    download_url = chosen.get("download_url")
    if not download_url:
        raise RuntimeError(f"Figshare file metadata did not include download_url: {chosen}")

    suffix = Path(str(chosen.get("name", "PAPILA.zip"))).suffix or ".zip"
    target_path = FIGSHARE_FALLBACK_DIR / f"PAPILA_figshare_v{version}{suffix}"
    if not target_path.exists():
        print(f"Downloading PAPILA from Figshare version {version} to: {target_path}")
        _download_with_progress(download_url, target_path)
    else:
        print(f"Reusing existing Figshare download: {target_path}")

    figshare_source = {
        "article_id": FIGSHARE_ARTICLE_ID,
        "version": version,
        "article_url": article.get("url_public_html") or f"https://figshare.com/articles/dataset/PAPILA/{FIGSHARE_ARTICLE_ID}",
        "file_name": chosen.get("name"),
        "download_url": download_url,
    }
    return target_path, figshare_source


def _bucket_for_patient(patient_id: int) -> int:
    digest = hashlib.sha1(str(patient_id).encode("utf-8")).hexdigest()
    return int(digest, 16) % 100


def _is_validation_patient(patient_id: int) -> bool:
    return _bucket_for_patient(patient_id) < VAL_PATIENT_PERCENT


def _resolve_papila_root(search_root: Path) -> Path:
    for candidate in [search_root] + sorted(search_root.rglob("*")):
        if not candidate.is_dir():
            continue
        if (candidate / "ClinicalData").exists() and (candidate / "FundusImages").exists():
            return candidate
    raise FileNotFoundError(f"Could not resolve extracted PAPILA root under: {search_root}")


def _extract_required_members(raw_zip: Path, extract_root: Path) -> Path:
    if extract_root.exists():
        shutil.rmtree(extract_root)
    extract_root.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(raw_zip) as archive:
        for member in archive.infolist():
            name = member.filename
            if member.is_dir():
                continue
            keep_member = False
            if "/FundusImages/" in name and name.lower().endswith(".jpg"):
                keep_member = True
            elif name.endswith("/ClinicalData/patient_data_od.xlsx"):
                keep_member = True
            elif name.endswith("/ClinicalData/patient_data_os.xlsx"):
                keep_member = True
            elif "/HelpCode/kfold/Test 2/" in name and name.lower().endswith(".xlsx"):
                keep_member = True
            if keep_member:
                archive.extract(member, extract_root)

    return _resolve_papila_root(extract_root)


def _fix_clinical_df(df):
    df_new = df.drop(["ID"], axis=0, errors="ignore").copy()
    df_new.columns = df_new.iloc[0, :]
    df_new = df_new[~df_new.index.isna()].copy()
    df_new.columns.name = "ID"
    return df_new


def _read_clinical_frames(papila_root: Path):
    pd = import_pandas()
    df_od = pd.read_excel(papila_root / "ClinicalData" / "patient_data_od.xlsx", index_col=[0])
    df_os = pd.read_excel(papila_root / "ClinicalData" / "patient_data_os.xlsx", index_col=[0])
    return _fix_clinical_df(df_od), _fix_clinical_df(df_os)


def _build_diagnosis_lookup(papila_root: Path) -> dict[tuple[int, str], int]:
    df_od, df_os = _read_clinical_frames(papila_root)
    lookup: dict[tuple[int, str], int] = {}

    for patient_key, row in df_od.iterrows():
        patient_id = int(str(patient_key).replace("#", ""))
        lookup[(patient_id, "OD")] = int(float(row["Diagnosis"]))

    for patient_key, row in df_os.iterrows():
        patient_id = int(str(patient_key).replace("#", ""))
        lookup[(patient_id, "OS")] = int(float(row["Diagnosis"]))

    return lookup


def _load_fold_records(papila_root: Path, fold_index: int, split_prefix: str) -> list[dict[str, int | str]]:
    pd = import_pandas()
    fold_path = (
        papila_root
        / "HelpCode"
        / "kfold"
        / "Test 2"
        / f"{split_prefix}_Test2_index_fold_{fold_index}.xlsx"
    )
    frame = pd.read_excel(fold_path)
    frame.columns = [str(column).strip() for column in frame.columns]

    records: list[dict[str, int | str]] = []
    for row in frame.itertuples(index=False):
        patient_id = int(float(getattr(row, "patID")))
        eye_id = int(float(getattr(row, "eyeID")))
        tag = int(float(getattr(row, "tags")))
        eye_code = "OD" if eye_id == 1 else "OS"
        records.append(
            {
                "patient_id": patient_id,
                "eye_code": eye_code,
                "eye_id": eye_id,
                "tag": tag,
            }
        )
    return records


def _extract_papila_binary_dataset(
    raw_zip: Path,
    extract_root: Path,
    dataset_root: Path,
) -> tuple[dict[str, dict[str, int]], dict[str, int]]:
    papila_root = _extract_required_members(raw_zip, extract_root)
    diagnosis_lookup = _build_diagnosis_lookup(papila_root)

    if dataset_root.exists():
        shutil.rmtree(dataset_root)
    dataset_root.mkdir(parents=True, exist_ok=True)

    counts = {
        "train": {"Healthy": 0, "Glaucoma": 0},
        "valid": {"Healthy": 0, "Glaucoma": 0},
        "test": {"Healthy": 0, "Glaucoma": 0},
    }

    source_counts = {
        "official_train_fold_rows": 0,
        "official_test_fold_rows": 0,
        "diagnosis_mismatches": 0,
    }

    split_records = {
        "train": _load_fold_records(papila_root, FOLD_INDEX, "tr"),
        "test": _load_fold_records(papila_root, FOLD_INDEX, "te"),
    }
    source_counts["official_train_fold_rows"] = len(split_records["train"])
    source_counts["official_test_fold_rows"] = len(split_records["test"])

    for fold_split, records in split_records.items():
        for record in records:
            patient_id = int(record["patient_id"])
            eye_code = str(record["eye_code"])
            fold_tag = int(record["tag"])
            file_name = f"RET{patient_id:03d}{eye_code}.jpg"
            diagnosis = diagnosis_lookup.get((patient_id, eye_code))
            if diagnosis is None:
                raise KeyError(f"Missing clinical diagnosis for {file_name}")
            if diagnosis not in {0, 1}:
                raise ValueError(
                    f"Unexpected suspicious/non-binary diagnosis inside official Test 2 fold for {file_name}: {diagnosis}"
                )
            if diagnosis != fold_tag:
                source_counts["diagnosis_mismatches"] += 1
                raise ValueError(
                    f"Diagnosis mismatch for {file_name}: clinical={diagnosis}, fold_tag={fold_tag}"
                )

            class_dir = "Healthy" if fold_tag == 0 else "Glaucoma"
            split_name = "test"
            if fold_split == "train":
                split_name = "valid" if _is_validation_patient(patient_id) else "train"

            source_path = papila_root / "FundusImages" / file_name
            if not source_path.exists():
                raise FileNotFoundError(f"Missing image file referenced by official fold: {source_path}")

            target_path = dataset_root / split_name / class_dir / file_name
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)
            counts[split_name][class_dir] += 1

    return counts, source_counts


def _collect_split_paths(dataset_root: Path, split_name: str) -> dict[str, list[Path]]:
    return {
        "Healthy": sorted((dataset_root / split_name / "Healthy").glob("*.jpg")),
        "Glaucoma": sorted((dataset_root / split_name / "Glaucoma").glob("*.jpg")),
    }


def _decode_image(path: tf.Tensor, label: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
    image = tf.io.read_file(path)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize_with_pad(image, IMAGE_SIZE[0], IMAGE_SIZE[1], antialias=True)
    image = tf.cast(image, tf.float32)
    label = tf.cast(label, tf.float32)
    return image, label


def make_balanced_train_dataset(dataset_root: Path) -> tuple[tf.data.Dataset, dict[str, int], int]:
    split_paths = _collect_split_paths(dataset_root, "train")
    counts = {
        "Healthy": len(split_paths["Healthy"]),
        "Glaucoma": len(split_paths["Glaucoma"]),
    }
    if not counts["Healthy"] or not counts["Glaucoma"]:
        raise RuntimeError(f"Training split must contain both classes, got: {counts}")

    max_count = max(counts.values())
    steps_per_epoch = math.ceil((2 * max_count) / BATCH_SIZE)

    def class_dataset(paths: list[Path], label: float) -> tf.data.Dataset:
        return (
            tf.data.Dataset.from_tensor_slices(
                (np.array([str(path) for path in paths]), np.full((len(paths),), label, dtype=np.float32))
            )
            .shuffle(len(paths), seed=SEED, reshuffle_each_iteration=True)
            .repeat()
        )

    healthy_ds = class_dataset(split_paths["Healthy"], 0.0)
    glaucoma_ds = class_dataset(split_paths["Glaucoma"], 1.0)
    train_ds = tf.data.Dataset.sample_from_datasets(
        [healthy_ds, glaucoma_ds],
        weights=[0.5, 0.5],
        seed=SEED,
    )
    train_ds = train_ds.map(_decode_image, num_parallel_calls=tf.data.AUTOTUNE)
    train_ds = train_ds.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
    return train_ds, counts, steps_per_epoch


def make_eval_dataset(dataset_root: Path, split_name: str) -> tf.data.Dataset:
    split_paths = _collect_split_paths(dataset_root, split_name)
    ordered_paths = [str(path) for path in split_paths["Healthy"]] + [
        str(path) for path in split_paths["Glaucoma"]
    ]
    ordered_labels = [0.0] * len(split_paths["Healthy"]) + [1.0] * len(split_paths["Glaucoma"])
    if not ordered_paths:
        raise RuntimeError(f"No evaluation images found for split: {split_name}")
    dataset = tf.data.Dataset.from_tensor_slices((ordered_paths, ordered_labels))
    dataset = dataset.map(_decode_image, num_parallel_calls=tf.data.AUTOTUNE)
    return dataset.batch(BATCH_SIZE).cache().prefetch(tf.data.AUTOTUNE)


def build_model() -> tuple[tf.keras.Model, tf.keras.Model]:
    augmentation = tf.keras.Sequential(
        [
            tf.keras.layers.RandomFlip("horizontal_and_vertical"),
            tf.keras.layers.RandomRotation(0.04),
            tf.keras.layers.RandomTranslation(0.05, 0.05),
            tf.keras.layers.RandomZoom(0.12),
            tf.keras.layers.RandomContrast(0.12),
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
    workdir = Path("/content/eyescan_papila_colab_v3")
    extract_root = workdir / "papila_raw_subset"
    dataset_root = workdir / "PAPILA_Glaucoma_vs_Healthy_OfficialFold"
    output_dir = drive_root / "EyeScan_Models" / "Fundus_Glaucoma_PAPILA_V3"
    workdir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_zip = _find_existing_raw_zip(datasets_root)
    figshare_source = None
    if raw_zip is None:
        raw_zip, figshare_source = _download_latest_figshare_papila()
    print("Using raw archive:", raw_zip)
    counts, source_counts = _extract_papila_binary_dataset(raw_zip, extract_root, dataset_root)
    print("Counts:", json.dumps(counts, indent=2))
    print("Official fold checks:", json.dumps(source_counts, indent=2))

    gpu_devices = tf.config.list_physical_devices("GPU")
    print("TensorFlow version:", tf.__version__)
    print("GPU devices:", gpu_devices)
    print("Mixed precision policy:", tf.keras.mixed_precision.global_policy())

    train_ds, train_sampler_counts, steps_per_epoch = make_balanced_train_dataset(dataset_root)
    val_ds = make_eval_dataset(dataset_root, "valid")
    test_ds = make_eval_dataset(dataset_root, "test")
    print("Balanced train sampler counts:", train_sampler_counts)
    print("Steps per epoch:", steps_per_epoch)

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
        steps_per_epoch=steps_per_epoch,
        epochs=FROZEN_EPOCHS,
        callbacks=callbacks,
        verbose=2,
    )

    _set_trainable_range(backbone, PARTIAL_UNFREEZE_LAYERS)
    compile_model(model, learning_rate=3e-5)
    history_partial = model.fit(
        train_ds,
        validation_data=val_ds,
        steps_per_epoch=steps_per_epoch,
        initial_epoch=len(history_frozen.history["loss"]),
        epochs=FROZEN_EPOCHS + PARTIAL_FINETUNE_EPOCHS,
        callbacks=callbacks,
        verbose=2,
    )

    _set_trainable_range(backbone, DEEP_UNFREEZE_LAYERS)
    compile_model(model, learning_rate=8e-6)
    history_deep = model.fit(
        train_ds,
        validation_data=val_ds,
        steps_per_epoch=steps_per_epoch,
        initial_epoch=len(history_frozen.history["loss"]) + len(history_partial.history["loss"]),
        epochs=FROZEN_EPOCHS + PARTIAL_FINETUNE_EPOCHS + DEEP_FINETUNE_EPOCHS,
        callbacks=callbacks,
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
        "class_names": CLASS_DIRS,
        "counts": counts,
        "source_counts": source_counts,
        "training_sampler": {
            "kind": "balanced_50_50_repeat",
            "source_train_counts": train_sampler_counts,
            "steps_per_epoch": steps_per_epoch,
        },
        "paper_protocol": {
            "binary_setup": "HelpCode/kfold/Test 2",
            "official_fold_index": FOLD_INDEX,
            "validation_patient_percent_from_official_train_fold": VAL_PATIENT_PERCENT,
            "correction_notice": "Nature article updated 2024-04-17; no dataset-label or split change is assumed in this image-only training recipe.",
        },
        "dataset_source": {
            "raw_archive_zip": str(raw_zip),
            "source_kind": "google_drive_upload" if figshare_source is None else "figshare_public_download",
            "figshare": figshare_source,
        },
        "device": {"gpu_count": len(gpu_devices), "gpu_names": [device.name for device in gpu_devices]},
        "history": {
            "frozen": round_history(history_frozen),
            "finetune_partial": round_history(history_partial),
            "finetune_deep": round_history(history_deep),
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
        "intended_use": "Image-only PAPILA healthy-vs-glaucoma candidate using the official binary fold split while staying deployable without expert contour inputs.",
        "deployment_status": "evaluation_only",
    }
    train_history = {
        "frozen": round_history(history_frozen),
        "finetune_partial": round_history(history_partial),
        "finetune_deep": round_history(history_deep),
    }
    train_config = {
        "run_name": RUN_NAME,
        "class_dirs": CLASS_DIRS,
        "image_size": list(IMAGE_SIZE),
        "batch_size": BATCH_SIZE,
        "frozen_epochs": FROZEN_EPOCHS,
        "partial_finetune_epochs": PARTIAL_FINETUNE_EPOCHS,
        "deep_finetune_epochs": DEEP_FINETUNE_EPOCHS,
        "early_stopping_patience": EARLY_STOPPING_PATIENCE,
        "official_binary_fold_index": FOLD_INDEX,
        "validation_patient_percent_within_official_train_fold": VAL_PATIENT_PERCENT,
        "partial_unfreeze_layers": PARTIAL_UNFREEZE_LAYERS,
        "deep_unfreeze_layers": DEEP_UNFREEZE_LAYERS,
        "raw_archive_zip": str(raw_zip),
        "raw_archive_source_kind": "google_drive_upload" if figshare_source is None else "figshare_public_download",
        "figshare_source": figshare_source,
        "output_dir": str(output_dir),
        "model_family": "efficientnetb2_imagenet",
        "train_sampler": "balanced_50_50_repeat",
        "resize_mode": "resize_with_pad",
        "preprocessing_tradeoff": "Uses full images rather than expert-disc ROI crops so the model stays compatible with future app/backend packaging.",
        "paper_correction_note": "Author correction published 2024-04-17; this recipe assumes no label, image, or fold semantics changed for Test 2.",
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
