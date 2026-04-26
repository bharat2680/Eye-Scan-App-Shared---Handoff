from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import random
import shutil
import zipfile
from pathlib import Path

import numpy as np
import tensorflow as tf


SEED = 42
RUN_NAME = "fundus_dr_idrid_v3_efficientnetb2_balanced_colab"
CLASS_DIRS = ["Healthy", "Diabetic Retinopathy"]
IMAGE_SIZE = (260, 260)
BATCH_SIZE = 12
FROZEN_EPOCHS = 6
PARTIAL_FINETUNE_EPOCHS = 10
DEEP_FINETUNE_EPOCHS = 8
EARLY_STOPPING_PATIENCE = 4
VAL_PERCENT = 20
PARTIAL_UNFREEZE_LAYERS = 120
DEEP_UNFREEZE_LAYERS = 220


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


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _bucket_for_name(name: str) -> int:
    digest = hashlib.sha1(name.encode("utf-8")).hexdigest()
    return int(digest, 16) % 100


def _is_validation_member(image_id: str) -> bool:
    return _bucket_for_name(image_id) < VAL_PERCENT


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
        datasets_root / "B. Disease Grading.zip",
        datasets_root / "B_Disease_Grading.zip",
        datasets_root / "idrid_disease_grading.zip",
    ]


def _find_existing_raw_zip(datasets_root: Path) -> Path:
    for candidate in _raw_zip_candidates(datasets_root):
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        "Expected one of: "
        + ", ".join(str(path) for path in _raw_zip_candidates(datasets_root))
    )


def _iter_csv_rows(archive: zipfile.ZipFile, member_name: str) -> list[dict[str, str]]:
    with archive.open(member_name) as handle:
        reader = csv.reader(io.TextIOWrapper(handle, encoding="utf-8"))
        header = next(reader)
        normalized_header = [cell.strip() for cell in header]
        rows = []
        for row in reader:
            if not row:
                continue
            padded = list(row) + [""] * max(0, len(normalized_header) - len(row))
            rows.append(dict(zip(normalized_header, padded)))
        return rows


def _extract_idrid_binary_dataset(raw_zip: Path, dataset_root: Path) -> dict[str, dict[str, int]]:
    if dataset_root.exists():
        shutil.rmtree(dataset_root)
    dataset_root.mkdir(parents=True, exist_ok=True)

    counts = {
        "train": {"Healthy": 0, "Diabetic Retinopathy": 0},
        "valid": {"Healthy": 0, "Diabetic Retinopathy": 0},
        "test": {"Healthy": 0, "Diabetic Retinopathy": 0},
    }

    with zipfile.ZipFile(raw_zip) as archive:
        train_labels_name = next(
            name for name in archive.namelist() if name.endswith("Training Labels.csv")
        )
        test_labels_name = next(
            name for name in archive.namelist() if name.endswith("Testing Labels.csv")
        )

        train_rows = _iter_csv_rows(archive, train_labels_name)
        test_rows = _iter_csv_rows(archive, test_labels_name)

        train_image_prefix = "B. Disease Grading/1. Original Images/a. Training Set/"
        test_image_prefix = "B. Disease Grading/1. Original Images/b. Testing Set/"

        def extract_rows(rows: list[dict[str, str]], image_prefix: str, split_kind: str) -> None:
            for row in rows:
                image_id = row["Image name"].strip()
                grade = int(row["Retinopathy grade"].strip())
                class_dir = "Healthy" if grade == 0 else "Diabetic Retinopathy"
                split_name = split_kind
                if split_kind == "train":
                    split_name = "valid" if _is_validation_member(image_id) else "train"
                target = dataset_root / split_name / class_dir / f"{image_id}.jpg"
                target.parent.mkdir(parents=True, exist_ok=True)
                member_name = f"{image_prefix}{image_id}.jpg"
                with archive.open(member_name) as src, target.open("wb") as dst:
                    shutil.copyfileobj(src, dst)
                counts[split_name][class_dir] += 1

        extract_rows(train_rows, train_image_prefix, "train")
        extract_rows(test_rows, test_image_prefix, "test")

    return counts


def _collect_split_paths(dataset_root: Path, split_name: str) -> dict[str, list[Path]]:
    return {
        "Healthy": sorted((dataset_root / split_name / "Healthy").glob("*.jpg")),
        "Diabetic Retinopathy": sorted((dataset_root / split_name / "Diabetic Retinopathy").glob("*.jpg")),
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
        "Diabetic Retinopathy": len(split_paths["Diabetic Retinopathy"]),
    }
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
    dr_ds = class_dataset(split_paths["Diabetic Retinopathy"], 1.0)
    train_ds = tf.data.Dataset.sample_from_datasets(
        [healthy_ds, dr_ds],
        weights=[0.5, 0.5],
        seed=SEED,
    )
    train_ds = train_ds.map(_decode_image, num_parallel_calls=tf.data.AUTOTUNE)
    train_ds = train_ds.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
    return train_ds, counts, steps_per_epoch


def make_eval_dataset(dataset_root: Path, split_name: str) -> tf.data.Dataset:
    split_paths = _collect_split_paths(dataset_root, split_name)
    ordered_paths = [str(path) for path in split_paths["Healthy"]] + [
        str(path) for path in split_paths["Diabetic Retinopathy"]
    ]
    ordered_labels = [0.0] * len(split_paths["Healthy"]) + [1.0] * len(split_paths["Diabetic Retinopathy"])
    dataset = tf.data.Dataset.from_tensor_slices((ordered_paths, ordered_labels))
    dataset = dataset.map(_decode_image, num_parallel_calls=tf.data.AUTOTUNE)
    return dataset.batch(BATCH_SIZE).cache().prefetch(tf.data.AUTOTUNE)


def build_model() -> tuple[tf.keras.Model, tf.keras.Model]:
    augmentation = tf.keras.Sequential(
        [
            tf.keras.layers.RandomFlip("horizontal"),
            tf.keras.layers.RandomRotation(0.04),
            tf.keras.layers.RandomTranslation(0.04, 0.04),
            tf.keras.layers.RandomZoom(0.12),
            tf.keras.layers.RandomContrast(0.15),
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
    labels = np.concatenate(
        [batch_labels.numpy().reshape(-1) for _, batch_labels in dataset],
        axis=0,
    ).astype(int)
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
    raw_zip = _find_existing_raw_zip(datasets_root)
    workdir = Path("/content/eyescan_idrid_colab_v3")
    dataset_root = workdir / "IDRiD_DR_vs_Healthy"
    output_dir = drive_root / "EyeScan_Models" / "Fundus_DR_IDRiD_V3"
    workdir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Using raw archive:", raw_zip)
    counts = _extract_idrid_binary_dataset(raw_zip, dataset_root)
    print("Counts:", json.dumps(counts, indent=2))

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
        "training_sampler": {
            "kind": "balanced_50_50_repeat",
            "source_train_counts": train_sampler_counts,
            "steps_per_epoch": steps_per_epoch,
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
    label_map = {"healthy": 0, "diabetic_retinopathy": 1}
    inference_contract = {
        "run_name": RUN_NAME,
        "model_file": "best_model.keras",
        "labels": ["healthy", "diabetic_retinopathy"],
        "input": {
            "image_size": list(IMAGE_SIZE),
            "color_mode": "rgb",
            "dtype": "float32",
            "resize_mode": "resize_with_pad",
            "normalization": "efficientnet_pretrained_internal_scaling",
        },
        "decision": {
            "rule": "threshold_on_positive_probability",
            "positive_label": "diabetic_retinopathy",
            "selected_threshold": selected_threshold,
            "selection_split": "val",
            "selection_objective": "balanced_accuracy",
            "argmax_fallback": True,
        },
        "intended_use": "Stronger evaluation-only fundus diabetic-retinopathy-vs-healthy screening candidate using IDRiD grading data.",
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
        "validation_percent_within_training_split": VAL_PERCENT,
        "partial_unfreeze_layers": PARTIAL_UNFREEZE_LAYERS,
        "deep_unfreeze_layers": DEEP_UNFREEZE_LAYERS,
        "raw_archive_zip": str(raw_zip),
        "output_dir": str(output_dir),
        "model_family": "efficientnetb2_imagenet",
        "train_sampler": "balanced_50_50_repeat",
        "resize_mode": "resize_with_pad",
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
