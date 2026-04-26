from __future__ import annotations

import json
import random
import shutil
import zipfile
from pathlib import Path

import numpy as np
import tensorflow as tf


SEED = 42
RUN_NAME = "fundus_glaucoma_eyefundus_v3_efficientnetb0_colab"
CLASS_NAMES = ["Healthy", "Glaucoma"]
SPLIT_DIRS = {"train": "train", "val": "valid", "test": "test"}
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
FROZEN_EPOCHS = 4
FINETUNE_EPOCHS = 6
EARLY_STOPPING_PATIENCE = 2


def seed_everything() -> None:
    random.seed(SEED)
    np.random.seed(SEED)
    tf.random.set_seed(SEED)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def has_expected_layout(root: Path) -> bool:
    return all((root / split / label).exists() for split in SPLIT_DIRS.values() for label in CLASS_NAMES)


def resolve_dataset_root(search_root: Path) -> Path:
    if has_expected_layout(search_root):
        return search_root
    for candidate in sorted(search_root.rglob("*")):
        if candidate.is_dir() and has_expected_layout(candidate):
            return candidate
    raise FileNotFoundError(f"Could not find extracted dataset root under: {search_root}")


def extract_filtered_zip(zip_path: Path, extract_root: Path) -> Path:
    if extract_root.exists():
        shutil.rmtree(extract_root)
    extract_root.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as archive:
        archive.extractall(extract_root)
    return resolve_dataset_root(extract_root)


def extract_from_raw_archive(zip_path: Path, extract_root: Path) -> Path:
    if extract_root.exists():
        shutil.rmtree(extract_root)
    extract_root.mkdir(parents=True, exist_ok=True)
    keep_splits = set(SPLIT_DIRS.values())
    keep_labels = set(CLASS_NAMES)
    extracted = 0
    with zipfile.ZipFile(zip_path) as archive:
        for member in archive.infolist():
            name = member.filename
            if member.is_dir() or not name.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
                continue
            parts = name.split("/")
            if len(parts) < 4 or parts[0] != "eye":
                continue
            split_name, label_name = parts[1], parts[2].strip()
            if split_name not in keep_splits or label_name not in keep_labels:
                continue
            target = extract_root / split_name / label_name / Path(parts[-1]).name
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(member) as src, target.open("wb") as dst:
                shutil.copyfileobj(src, dst)
            extracted += 1
    if extracted == 0:
        raise RuntimeError(f"No Glaucoma/Healthy images were extracted from: {zip_path}")
    return extract_root


def count_images(dataset_root: Path) -> dict[str, dict[str, int]]:
    counts: dict[str, dict[str, int]] = {}
    for split_name, split_dir in SPLIT_DIRS.items():
        counts[split_name] = {}
        for class_name in CLASS_NAMES:
            class_dir = dataset_root / split_dir / class_name
            counts[split_name][class_name] = len(
                [
                    path
                    for path in class_dir.rglob("*")
                    if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png"}
                ]
            )
    return counts


def compute_class_weights(train_counts: dict[str, int]) -> dict[int, float]:
    label_counts = {
        0: int(train_counts["Healthy"]),
        1: int(train_counts["Glaucoma"]),
    }
    total = sum(label_counts.values())
    return {label: total / (2 * max(count, 1)) for label, count in label_counts.items()}


def make_split_dataset(dataset_root: Path, split_name: str, training: bool) -> tf.data.Dataset:
    split_dir = dataset_root / SPLIT_DIRS[split_name]
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
            tf.keras.layers.RandomZoom(0.08),
            tf.keras.layers.RandomContrast(0.1),
        ],
        name="augmentation",
    )
    backbone = tf.keras.applications.EfficientNetB0(
        include_top=False,
        weights="imagenet",
        input_shape=IMAGE_SIZE + (3,),
        pooling="avg",
    )
    backbone.trainable = False

    inputs = tf.keras.Input(shape=IMAGE_SIZE + (3,))
    x = augmentation(inputs)
    x = backbone(x, training=False)
    x = tf.keras.layers.Dropout(0.35)(x)
    outputs = tf.keras.layers.Dense(1, activation="sigmoid")(x)
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    return model, backbone


def compile_model(model: tf.keras.Model, learning_rate: float) -> None:
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss="binary_crossentropy",
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
    for threshold in np.linspace(0.05, 0.95, 19):
        confusion = confusion_for_threshold(y_true, y_prob, float(threshold))
        score = balanced_accuracy_from_confusion(confusion)
        if score > best_score:
            best_score = score
            best_threshold = float(round(threshold, 2))
            best_confusion = confusion
    return best_threshold, best_score, best_confusion


def round_history(history: tf.keras.callbacks.History) -> dict[str, list[float]]:
    return {key: [round(float(value), 6) for value in values] for key, values in history.history.items()}


def main() -> None:
    from google.colab import drive

    drive.mount("/content/drive")

    seed_everything()

    drive_root = Path("/content/drive/MyDrive")
    datasets_root = drive_root / "Datasets"
    preferred_zip = datasets_root / "eye_fundus_glaucoma_vs_healthy.zip"
    raw_archive = datasets_root / "Eye-Fundus.zip"
    workdir = Path("/content/eyescan_fundus_colab")
    extract_root = workdir / "Eye_Fundus_Glaucoma_vs_Healthy"
    output_dir = drive_root / "EyeScan_Models" / "Fundus_Glaucoma_EyeFundus_V3"
    output_dir.mkdir(parents=True, exist_ok=True)
    workdir.mkdir(parents=True, exist_ok=True)

    print("Drive roots:")
    for path in [datasets_root, output_dir]:
        print(f"  - {path} :: exists={path.exists()}")

    if has_expected_layout(extract_root):
        dataset_root = extract_root
        print(f"Using existing extracted dataset at: {dataset_root}")
    elif preferred_zip.exists():
        print(f"Extracting preferred filtered dataset from: {preferred_zip}")
        dataset_root = extract_filtered_zip(preferred_zip, extract_root)
    elif raw_archive.exists():
        print(f"Extracting glaucoma/healthy subset from raw archive: {raw_archive}")
        dataset_root = extract_from_raw_archive(raw_archive, extract_root)
    else:
        raise FileNotFoundError(
            "Expected either /content/drive/MyDrive/Datasets/eye_fundus_glaucoma_vs_healthy.zip "
            "or /content/drive/MyDrive/Datasets/Eye-Fundus.zip"
        )

    gpu_devices = tf.config.list_physical_devices("GPU")
    print("TensorFlow version:", tf.__version__)
    print("GPU devices:", gpu_devices)

    counts = count_images(dataset_root)
    class_weights = compute_class_weights(counts["train"])
    print("Counts:", json.dumps(counts, indent=2))
    print("Class weights:", class_weights)

    train_ds = make_split_dataset(dataset_root, "train", training=True)
    val_ds = make_split_dataset(dataset_root, "val", training=False)
    test_ds = make_split_dataset(dataset_root, "test", training=False)

    best_model_path = output_dir / "best_model.keras"
    model, backbone = build_model()
    compile_model(model, learning_rate=3e-4)
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=EARLY_STOPPING_PATIENCE,
            restore_best_weights=True,
        ),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=best_model_path,
            monitor="val_loss",
            save_best_only=True,
        ),
    ]

    history_frozen = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=FROZEN_EPOCHS,
        class_weight=class_weights,
        callbacks=callbacks,
        verbose=2,
    )

    backbone.trainable = True
    for layer in backbone.layers[:-40]:
        layer.trainable = False
    compile_model(model, learning_rate=1e-5)

    history_finetune = model.fit(
        train_ds,
        validation_data=val_ds,
        initial_epoch=len(history_frozen.history["loss"]),
        epochs=FROZEN_EPOCHS + FINETUNE_EPOCHS,
        class_weight=class_weights,
        callbacks=callbacks,
        verbose=2,
    )

    model = tf.keras.models.load_model(best_model_path)

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
        "class_weights": {str(key): float(value) for key, value in class_weights.items()},
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
        "input_size": list(IMAGE_SIZE),
        "input_channels": 3,
        "class_folders": CLASS_NAMES,
        "positive_class_folder": "Glaucoma",
        "positive_threshold": selected_threshold,
        "model_family": "efficientnetb0_imagenet",
    }
    train_history = {
        "frozen": round_history(history_frozen),
        "finetune": round_history(history_finetune),
    }
    train_config = {
        "run_name": RUN_NAME,
        "class_names": CLASS_NAMES,
        "split_dirs": SPLIT_DIRS,
        "image_size": list(IMAGE_SIZE),
        "batch_size": BATCH_SIZE,
        "frozen_epochs": FROZEN_EPOCHS,
        "finetune_epochs": FINETUNE_EPOCHS,
        "early_stopping_patience": EARLY_STOPPING_PATIENCE,
        "preferred_filtered_zip": str(preferred_zip),
        "raw_archive_zip": str(raw_archive),
        "output_dir": str(output_dir),
        "model_family": "efficientnetb0_imagenet",
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
