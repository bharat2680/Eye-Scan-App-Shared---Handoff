import argparse
import hashlib
import json
import math
import random
from collections import Counter
from pathlib import Path

import numpy as np
import tensorflow as tf


SEED = 42


def parse_args():
    parser = argparse.ArgumentParser(description="Train a binary image classifier from class-folder datasets.")
    parser.add_argument("--config", type=Path, required=True, help="Path to JSON config.")
    return parser.parse_args()


def load_config(config_path: Path) -> dict:
    with config_path.open("r", encoding="utf-8") as handle:
        config = json.load(handle)
    config["config_path"] = str(config_path)
    return config


def validate_config(config: dict) -> None:
    required = [
        "run_name",
        "dataset_root",
        "output_dir",
        "class_folders",
        "positive_class_folder",
    ]
    missing = [key for key in required if key not in config]
    if missing:
        raise SystemExit(f"Missing config keys: {missing}")
    if len(config["class_folders"]) != 2:
        raise SystemExit("Binary training expects exactly two class folders.")
    if config["positive_class_folder"] not in config["class_folders"]:
        raise SystemExit("positive_class_folder must be one of class_folders.")
    if config.get("use_predefined_splits", False):
        split_dirs = config.get("predefined_split_dirs", {})
        required_splits = {"train", "val", "test"}
        missing_split_dirs = sorted(required_splits - set(split_dirs))
        if missing_split_dirs:
            raise SystemExit(f"Missing predefined_split_dirs entries: {missing_split_dirs}")


def deterministic_split_key(path: Path) -> int:
    digest = hashlib.sha1(str(path).encode("utf-8")).hexdigest()
    return int(digest, 16) % 100


def assign_split(path: Path, train_pct: int, val_pct: int) -> str:
    bucket = deterministic_split_key(path)
    if bucket < train_pct:
        return "train"
    if bucket < train_pct + val_pct:
        return "val"
    return "test"


def discover_samples(config: dict) -> tuple[list[dict], dict]:
    dataset_root = Path(config["dataset_root"]).expanduser()
    class_folders = config["class_folders"]
    positive_folder = config["positive_class_folder"]
    use_predefined_splits = bool(config.get("use_predefined_splits", False))
    train_pct = int(config.get("train_percent", 70))
    val_pct = int(config.get("val_percent", 15))

    samples: list[dict] = []
    counts = {"train": Counter(), "val": Counter(), "test": Counter()}

    if use_predefined_splits:
        split_dirs = config["predefined_split_dirs"]
        for split_name, split_dir_name in split_dirs.items():
            split_root = dataset_root / split_dir_name
            if not split_root.exists():
                raise SystemExit(f"Predefined split folder not found: {split_root}")
            for class_name in class_folders:
                class_dir = split_root / class_name
                if not class_dir.exists():
                    raise SystemExit(f"Class folder not found: {class_dir}")
                label = 1 if class_name == positive_folder else 0
                image_paths = sorted(
                    path
                    for path in class_dir.rglob("*")
                    if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png"}
                )
                for image_path in image_paths:
                    record = {
                        "path": image_path,
                        "class_name": class_name,
                        "label": label,
                        "split": split_name,
                    }
                    samples.append(record)
                    counts[split_name][class_name] += 1
    else:
        for class_name in class_folders:
            class_dir = dataset_root / class_name
            if not class_dir.exists():
                raise SystemExit(f"Class folder not found: {class_dir}")
            label = 1 if class_name == positive_folder else 0
            image_paths = sorted(
                path
                for path in class_dir.rglob("*")
                if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png"}
            )
            for image_path in image_paths:
                split = assign_split(image_path, train_pct=train_pct, val_pct=val_pct)
                record = {
                    "path": image_path,
                    "class_name": class_name,
                    "label": label,
                    "split": split,
                }
                samples.append(record)
                counts[split][class_name] += 1

    return samples, counts


def ensure_viable_splits(counts: dict) -> None:
    for split_name in ("train", "val", "test"):
        if len(counts[split_name]) < 2:
            raise SystemExit(f"{split_name} split is missing one of the two classes: {counts[split_name]}")
        if min(counts[split_name].values()) < 1:
            raise SystemExit(f"{split_name} split has an empty class: {counts[split_name]}")


def make_dataset(rows: list[dict], image_size: tuple[int, int], batch_size: int, training: bool):
    paths = tf.constant([str(row["path"]) for row in rows])
    labels = tf.constant([row["label"] for row in rows], dtype=tf.float32)
    dataset = tf.data.Dataset.from_tensor_slices((paths, labels))

    def _load(path, label):
        image = tf.io.read_file(path)
        image = tf.image.decode_image(image, channels=3, expand_animations=False)
        image = tf.image.resize(image, image_size)
        image = tf.cast(image, tf.float32) / 255.0
        return image, label

    dataset = dataset.map(_load, num_parallel_calls=tf.data.AUTOTUNE)
    if training:
        dataset = dataset.shuffle(buffer_size=max(len(rows), 1), seed=SEED, reshuffle_each_iteration=True)
    return dataset.batch(batch_size).prefetch(tf.data.AUTOTUNE)


def build_model(
    image_size: tuple[int, int],
    dropout_rate: float,
    conv_filters: list[int],
    augment_train: bool,
) -> tf.keras.Model:
    inputs = tf.keras.Input(shape=image_size + (3,))
    x = inputs
    if augment_train:
        x = tf.keras.Sequential(
            [
                tf.keras.layers.RandomFlip("horizontal"),
                tf.keras.layers.RandomRotation(0.03),
                tf.keras.layers.RandomZoom(0.08),
            ],
            name="augmentation",
        )(x)
    for index, filters in enumerate(conv_filters):
        x = tf.keras.layers.Conv2D(filters, 3, padding="same", activation="relu", name=f"conv_{index+1}")(x)
        if index < len(conv_filters) - 1:
            x = tf.keras.layers.MaxPooling2D(name=f"pool_{index+1}")(x)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(dropout_rate)(x)
    outputs = tf.keras.layers.Dense(1, activation="sigmoid")(x)
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    return model


def compute_class_weights(rows: list[dict]) -> dict:
    counts = Counter(row["label"] for row in rows)
    total = sum(counts.values())
    return {label: total / (2 * max(count, 1)) for label, count in counts.items()}


def oversample_minority(rows: list[dict]) -> tuple[list[dict], dict]:
    by_label: dict[int, list[dict]] = {0: [], 1: []}
    for row in rows:
        by_label[row["label"]].append(row)
    max_count = max(len(by_label[0]), len(by_label[1]))
    balanced: list[dict] = []
    effective_counts = {}
    for label, label_rows in by_label.items():
        if not label_rows:
            continue
        repeats = math.ceil(max_count / len(label_rows))
        expanded = (label_rows * repeats)[:max_count]
        balanced.extend(expanded)
        effective_counts[str(label)] = len(expanded)
    random.Random(SEED).shuffle(balanced)
    return balanced, effective_counts


def collect_predictions(model: tf.keras.Model, dataset):
    probabilities = model.predict(dataset, verbose=0).reshape(-1)
    labels = np.concatenate([labels.numpy() for _, labels in dataset], axis=0)
    return probabilities, labels.astype(int)


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


def scalar_history(history: tf.keras.callbacks.History) -> dict:
    return {key: [float(value) for value in values] for key, values in history.history.items()}


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main():
    args = parse_args()
    config = load_config(args.config)
    validate_config(config)

    random.seed(SEED)
    np.random.seed(SEED)
    tf.random.set_seed(SEED)

    image_size = tuple(config.get("image_size", [224, 224]))
    batch_size = int(config.get("batch_size", 16))
    epochs = int(config.get("epochs", 8))
    learning_rate = float(config.get("learning_rate", 1e-3))
    dropout_rate = float(config.get("dropout_rate", 0.3))
    conv_filters = [int(value) for value in config.get("conv_filters", [32, 64, 128])]
    augment_train = bool(config.get("augment_train", False))
    output_dir = Path(config["output_dir"]).expanduser()

    samples, counts = discover_samples(config)
    ensure_viable_splits(counts)

    train_rows = [row for row in samples if row["split"] == "train"]
    val_rows = [row for row in samples if row["split"] == "val"]
    test_rows = [row for row in samples if row["split"] == "test"]

    effective_train_rows = train_rows
    effective_train_counts = None
    if config.get("oversample_minority_train", False):
        effective_train_rows, effective_train_counts = oversample_minority(train_rows)

    train_ds = make_dataset(effective_train_rows, image_size=image_size, batch_size=batch_size, training=True)
    val_ds = make_dataset(val_rows, image_size=image_size, batch_size=batch_size, training=False)
    test_ds = make_dataset(test_rows, image_size=image_size, batch_size=batch_size, training=False)

    model = build_model(
        image_size=image_size,
        dropout_rate=dropout_rate,
        conv_filters=conv_filters,
        augment_train=augment_train,
    )
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss="binary_crossentropy",
        metrics=["accuracy", tf.keras.metrics.AUC(name="auc")],
    )

    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss", patience=int(config.get("early_stopping_patience", 3)), restore_best_weights=True
        )
    ]

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        class_weight=compute_class_weights(effective_train_rows),
        callbacks=callbacks,
        verbose=2,
    )

    val_prob, val_true = collect_predictions(model, val_ds)
    test_prob, test_true = collect_predictions(model, test_ds)
    selected_threshold, val_bal_acc, val_confusion = find_best_threshold(val_true, val_prob)
    default_test_confusion = confusion_for_threshold(test_true, test_prob, 0.5)
    tuned_test_confusion = confusion_for_threshold(test_true, test_prob, selected_threshold)

    metrics = {
        "run_name": config["run_name"],
        "dataset_root": config["dataset_root"],
        "counts": {split: dict(counter) for split, counter in counts.items()},
        "train_rows": len(train_rows),
        "effective_train_rows": len(effective_train_rows),
        "effective_train_counts": effective_train_counts,
        "val_rows": len(val_rows),
        "test_rows": len(test_rows),
        "history": scalar_history(history),
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

    positive_class_folder = config["positive_class_folder"]
    negative_class_folder = next(name for name in config["class_folders"] if name != positive_class_folder)
    label_map = {
        config.get("negative_label", negative_class_folder.lower().replace(" ", "_")): 0,
        config.get("positive_label", positive_class_folder.lower().replace(" ", "_")): 1,
    }
    inference_contract = {
        "input_size": list(image_size),
        "input_channels": 3,
        "normalization": "rescale_1_over_255",
        "positive_threshold": selected_threshold,
        "class_folders": config["class_folders"],
        "positive_class_folder": positive_class_folder,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    model.save(output_dir / "best_model.keras")
    write_json(output_dir / "metrics.json", metrics)
    write_json(output_dir / "label_map.json", label_map)
    write_json(output_dir / "train_config.json", config)
    write_json(output_dir / "inference_contract.json", inference_contract)

    print(json.dumps(metrics, indent=2))
    print(f"Saved model to: {output_dir / 'best_model.keras'}")


if __name__ == "__main__":
    main()
