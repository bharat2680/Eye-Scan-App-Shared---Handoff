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
RUN_NAME = "fundus_glaucoma_rimone_v1_vgg19_byhospital_colab"
CLASS_NAMES = ["Healthy", "Glaucoma"]
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 16
FROZEN_EPOCHS = 5
FINETUNE_EPOCHS = 10
EARLY_STOPPING_PATIENCE = 3
VAL_PERCENT = 20
PARTITION_VARIANT = "by_hospital"
RIM_ONE_IMAGES_SHORT_URL = "https://bit.ly/rim-one-dl-images"
DOWNLOAD_CACHE_DIR = Path("/content/rim_one_downloads")


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


def import_gdown():
    try:
        import gdown
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "gdown"], check=True)
        import gdown
    return gdown


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
        datasets_root / "rim-one-dl-images.zip",
        datasets_root / "RIM-ONE-DL-images.zip",
        datasets_root / "RIM-ONE_DL_images.zip",
        datasets_root / "rim_one_dl_images.zip",
    ]


def _find_existing_raw_zip(datasets_root: Path) -> Path | None:
    for candidate in _drive_zip_candidates(datasets_root):
        if candidate.exists():
            return candidate
    return None


def _resolve_final_url(url: str) -> str:
    request = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(request) as response:
            return response.geturl()
    except Exception:
        with urllib.request.urlopen(url) as response:
            return response.geturl()


def _extract_google_drive_file_id(url: str) -> str | None:
    patterns = [
        r"/file/d/([a-zA-Z0-9_-]+)",
        r"[?&]id=([a-zA-Z0-9_-]+)",
        r"/uc\?export=download&id=([a-zA-Z0-9_-]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
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


def _download_official_rimone_images() -> tuple[Path, dict]:
    DOWNLOAD_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    resolved_url = _resolve_final_url(RIM_ONE_IMAGES_SHORT_URL)
    target_path = DOWNLOAD_CACHE_DIR / "rim_one_dl_images_official.zip"
    if not target_path.exists():
        if "drive.google.com" in resolved_url:
            file_id = _extract_google_drive_file_id(resolved_url)
            if not file_id:
                raise RuntimeError(f"Could not extract Google Drive file id from: {resolved_url}")
            print(f"Downloading RIM-ONE DL images from official Google Drive target: {resolved_url}")
            gdown = import_gdown()
            gdown.download(id=file_id, output=str(target_path), quiet=False, fuzzy=True)
        else:
            print(f"Downloading RIM-ONE DL images from official URL: {resolved_url}")
            _download_with_progress(resolved_url, target_path)
    else:
        print(f"Reusing existing downloaded archive: {target_path}")

    source_info = {
        "source_kind": "official_repo_download_link",
        "official_entry_point": RIM_ONE_IMAGES_SHORT_URL,
        "resolved_url": resolved_url,
    }
    return target_path, source_info


def _bucket_for_name(name: str) -> int:
    digest = hashlib.sha1(name.encode("utf-8")).hexdigest()
    return int(digest, 16) % 100


def _is_validation_member(image_id: str) -> bool:
    return _bucket_for_name(image_id) < VAL_PERCENT


def _normalize_token(part: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", part.lower())


def _infer_variant(parts: tuple[str, ...]) -> str | None:
    tokens = [_normalize_token(part) for part in parts]
    if any("hospital" in token for token in tokens):
        return "by_hospital"
    if any("random" in token for token in tokens):
        return "random"
    return None


def _infer_split(parts: tuple[str, ...], variant: str | None) -> str | None:
    tokens = [_normalize_token(part) for part in parts]
    if any("train" in token for token in tokens):
        return "train"
    if any("test" in token for token in tokens):
        return "test"
    if variant == "by_hospital":
        if any(token == "huc" or token.endswith("huc") or token.startswith("huc") for token in tokens):
            return "train"
        if any(token == "hums" or token == "hcsc" or token.endswith("hums") or token.endswith("hcsc") for token in tokens):
            return "test"
    return None


def _infer_class(parts: tuple[str, ...]) -> str | None:
    tokens = [_normalize_token(part) for part in parts]
    if any("glaucoma" in token or "glaucomatous" in token for token in tokens):
        return "Glaucoma"
    if any(token == "normal" or token == "healthy" or "normal" in token or "healthy" in token for token in tokens):
        return "Healthy"
    return None


def _extract_rimone_dataset(raw_zip: Path, raw_extract_root: Path, dataset_root: Path) -> tuple[dict[str, dict[str, int]], dict]:
    if raw_extract_root.exists():
        shutil.rmtree(raw_extract_root)
    if dataset_root.exists():
        shutil.rmtree(dataset_root)
    raw_extract_root.mkdir(parents=True, exist_ok=True)
    dataset_root.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(raw_zip) as archive:
        archive.extractall(raw_extract_root)

    counts = {
        "train": {"Healthy": 0, "Glaucoma": 0},
        "valid": {"Healthy": 0, "Glaucoma": 0},
        "test": {"Healthy": 0, "Glaucoma": 0},
    }
    debug = {
        "selected_partition_variant": PARTITION_VARIANT,
        "matched_images": 0,
        "variant_hits": {"by_hospital": 0, "random": 0, "unknown": 0},
        "sample_unmatched_paths": [],
    }

    image_suffixes = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}
    for path in sorted(raw_extract_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in image_suffixes:
            continue
        relative = path.relative_to(raw_extract_root)
        parts = relative.parts[:-1]
        variant = _infer_variant(parts)
        split = _infer_split(parts, variant)
        class_name = _infer_class(parts)
        variant_key = variant if variant is not None else "unknown"
        debug["variant_hits"][variant_key] += 1

        if variant != PARTITION_VARIANT or split is None or class_name is None:
            if len(debug["sample_unmatched_paths"]) < 25:
                debug["sample_unmatched_paths"].append(str(relative))
            continue

        final_split = split
        image_id = path.stem
        if split == "train":
            final_split = "valid" if _is_validation_member(image_id) else "train"

        target_path = dataset_root / final_split / class_name / path.name
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target_path)
        counts[final_split][class_name] += 1
        debug["matched_images"] += 1

    if debug["matched_images"] == 0:
        raise RuntimeError(
            "No images were extracted for the selected RIM-ONE DL partition. "
            f"Variant hits: {debug['variant_hits']}. Sample unmatched paths: {debug['sample_unmatched_paths']}"
        )

    return counts, debug


def compute_class_weights(train_counts: dict[str, int]) -> dict[int, float]:
    label_counts = {0: int(train_counts["Healthy"]), 1: int(train_counts["Glaucoma"])}
    total = sum(label_counts.values())
    return {label: total / (2 * max(count, 1)) for label, count in label_counts.items()}


def _preprocess_images(images: tf.Tensor, labels: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
    images = tf.cast(images, tf.float32)
    images = tf.keras.applications.vgg19.preprocess_input(images)
    labels = tf.cast(labels, tf.float32)
    return images, labels


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
    dataset = dataset.map(_preprocess_images, num_parallel_calls=tf.data.AUTOTUNE)
    return dataset.prefetch(tf.data.AUTOTUNE)


def build_model() -> tuple[tf.keras.Model, tf.keras.Model]:
    augmentation = tf.keras.Sequential(
        [
            tf.keras.layers.RandomFlip("horizontal"),
            tf.keras.layers.RandomRotation(0.03),
            tf.keras.layers.RandomZoom(0.08),
            tf.keras.layers.RandomContrast(0.10),
        ],
        name="augmentation",
    )
    backbone = tf.keras.applications.VGG19(
        include_top=False,
        weights="imagenet",
        input_shape=IMAGE_SIZE + (3,),
        pooling="avg",
    )
    backbone.trainable = False

    inputs = tf.keras.Input(shape=IMAGE_SIZE + (3,))
    x = augmentation(inputs)
    x = tf.keras.applications.vgg19.preprocess_input(x)
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
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss=tf.keras.losses.BinaryCrossentropy(label_smoothing=0.01),
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


def _set_finetune_layers(backbone: tf.keras.Model) -> None:
    backbone.trainable = True
    trainable = False
    for layer in backbone.layers:
        if layer.name == "block5_conv1":
            trainable = True
        layer.trainable = trainable


def main() -> None:
    from google.colab import drive

    drive.mount("/content/drive")
    seed_everything()
    enable_mixed_precision_if_gpu()

    drive_root = Path("/content/drive/MyDrive")
    datasets_root = drive_root / "Datasets"
    output_dir = drive_root / "EyeScan_Models" / "Fundus_Glaucoma_RIM_ONE_DL_V1"
    workdir = Path("/content/eyescan_rimone_colab_v1")
    raw_extract_root = workdir / "rimone_raw"
    dataset_root = workdir / "RIM_ONE_Glaucoma_vs_Healthy"
    workdir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_zip = _find_existing_raw_zip(datasets_root)
    source_info = None
    if raw_zip is None:
        raw_zip, source_info = _download_official_rimone_images()
    else:
        source_info = {
            "source_kind": "google_drive_upload",
            "official_entry_point": RIM_ONE_IMAGES_SHORT_URL,
            "resolved_url": None,
        }

    print("Using raw archive:", raw_zip)
    counts, debug = _extract_rimone_dataset(raw_zip, raw_extract_root, dataset_root)
    print("Counts:", json.dumps(counts, indent=2))
    print("Layout debug:", json.dumps(debug, indent=2))

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

    compile_model(model, learning_rate=1e-4)
    history_frozen = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=FROZEN_EPOCHS,
        callbacks=callbacks,
        class_weight=class_weights,
        verbose=2,
    )

    _set_finetune_layers(backbone)
    compile_model(model, learning_rate=1e-5)
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
            "dataset": "RIM-ONE DL",
            "partition_variant": PARTITION_VARIANT,
            "official_repo_entry_point": "https://github.com/miag-ull/rim-one-dl",
            "official_images_download_entry": RIM_ONE_IMAGES_SHORT_URL,
        },
        "dataset_source": {
            "raw_archive_zip": str(raw_zip),
            **source_info,
        },
        "layout_debug": debug,
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
            "resize_mode": "resize",
            "normalization": "vgg19_caffe_preprocess",
        },
        "decision": {
            "rule": "threshold_on_positive_probability",
            "positive_label": "glaucoma",
            "selected_threshold": selected_threshold,
            "selection_split": "val",
            "selection_objective": "balanced_accuracy",
            "argmax_fallback": True,
        },
        "intended_use": "Evaluation-only glaucoma-vs-healthy screening candidate using the official RIM-ONE DL by-hospital partition.",
        "deployment_status": "evaluation_only",
    }
    train_history = {
        "frozen": round_history(history_frozen),
        "finetune": round_history(history_finetune),
    }
    train_config = {
        "run_name": RUN_NAME,
        "partition_variant": PARTITION_VARIANT,
        "class_names": CLASS_NAMES,
        "image_size": list(IMAGE_SIZE),
        "batch_size": BATCH_SIZE,
        "frozen_epochs": FROZEN_EPOCHS,
        "finetune_epochs": FINETUNE_EPOCHS,
        "early_stopping_patience": EARLY_STOPPING_PATIENCE,
        "validation_percent_within_official_training_split": VAL_PERCENT,
        "raw_archive_zip": str(raw_zip),
        "output_dir": str(output_dir),
        "model_family": "vgg19_imagenet_gap_sigmoid",
        "class_weighting": class_weights,
        "preprocessing": "vgg19_caffe_preprocess",
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
