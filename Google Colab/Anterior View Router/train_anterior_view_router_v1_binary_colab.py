from __future__ import annotations

import json
import math
import random
import shutil
import subprocess
import sys
import zipfile
from collections import Counter
from pathlib import Path

import numpy as np


def ensure_dependencies() -> None:
    required = {
        "tensorflow": "tensorflow",
        "pandas": "pandas",
        "sklearn": "scikit-learn",
        "matplotlib": "matplotlib",
        "PIL": "pillow",
    }
    missing = []
    for module_name, package_name in required.items():
        try:
            __import__(module_name)
        except ImportError:
            missing.append(package_name)
    if missing:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", *missing], check=True)


ensure_dependencies()

import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
from PIL import Image
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score


SEED = 42
RUN_NAME = "anterior_view_router_v1_mobilenetv2_binary_colab"
CLASS_NAMES = ["eyelid_dominant", "iris_visible"]
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
FROZEN_EPOCHS = 5
FINETUNE_EPOCHS = 8
EARLY_STOPPING_PATIENCE = 3
INITIAL_LEARNING_RATE = 1e-3
FINETUNE_LEARNING_RATE = 1e-4
FINE_TUNE_AT = 80
IRIS_VISIBLE_MIN_PROBABILITY = 0.65
EYELID_DOMINANT_MAX_PROBABILITY = 0.35
FALLBACK_REASON = "low_confidence_view_route"


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


def mount_drive():
    from google.colab import drive

    drive.mount("/content/drive", force_remount=False)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def sanitize_keras_archive(model_path: Path) -> None:
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


def locate_dataset_zip(drive_root: Path) -> Path:
    candidates = [
        drive_root / "EyeScan_Models" / "Colab_Datasets" / "anterior_view_router_v1_binary_colab_dataset.zip",
        drive_root / "EyeScan_Models" / "colab_datasets" / "anterior_view_router_v1_binary_colab_dataset.zip",
        drive_root / "Datasets" / "anterior_view_router_v1_binary_colab_dataset.zip",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        "Could not find anterior_view_router_v1_binary_colab_dataset.zip in the expected Drive locations."
    )


def extract_dataset(zip_path: Path, extract_root: Path) -> Path:
    if extract_root.exists():
        shutil.rmtree(extract_root)
    extract_root.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as archive:
        archive.extractall(extract_root)

    children = [child for child in extract_root.iterdir() if child.is_dir()]
    if len(children) != 1:
        raise RuntimeError(f"Expected exactly one dataset folder inside {zip_path}, found {len(children)}")
    return children[0]


def make_dataset(split_dir: Path, training: bool) -> tf.data.Dataset:
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
    if list(dataset.class_names) != CLASS_NAMES:
        raise RuntimeError(f"Unexpected class order: {dataset.class_names}")
    return dataset


def count_dataset_files(split_dir: Path) -> dict[str, int]:
    counts = {}
    for class_name in CLASS_NAMES:
        class_dir = split_dir / class_name
        counts[class_name] = len([path for path in class_dir.iterdir() if path.is_file()]) if class_dir.exists() else 0
    return counts


def build_class_weights(train_counts: dict[str, int]) -> dict[int, float]:
    total = sum(train_counts.values())
    num_classes = len(CLASS_NAMES)
    weights = {}
    for idx, class_name in enumerate(CLASS_NAMES):
        count = train_counts[class_name]
        if count <= 0:
            raise RuntimeError(f"Train split for {class_name} is empty.")
        weights[idx] = total / (num_classes * count)
    return weights


def build_model() -> tf.keras.Model:
    preprocess = tf.keras.applications.mobilenet_v2.preprocess_input
    augmentation = tf.keras.Sequential(
        [
            tf.keras.layers.RandomFlip("horizontal"),
            tf.keras.layers.RandomRotation(0.03),
            tf.keras.layers.RandomZoom(0.05),
            tf.keras.layers.RandomContrast(0.10),
        ],
        name="augmentation",
    )

    inputs = tf.keras.Input(shape=(*IMAGE_SIZE, 3), name="image")
    x = augmentation(inputs)
    x = preprocess(x)
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(*IMAGE_SIZE, 3),
        include_top=False,
        weights="imagenet",
    )
    base_model.trainable = False
    x = base_model(x, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(0.30)(x)
    outputs = tf.keras.layers.Dense(1, activation="sigmoid", dtype="float32", name="iris_visible_probability")(x)
    model = tf.keras.Model(inputs=inputs, outputs=outputs, name=RUN_NAME)
    return model


def compile_model(model: tf.keras.Model, learning_rate: float) -> None:
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss=tf.keras.losses.BinaryCrossentropy(),
        metrics=[
            tf.keras.metrics.BinaryAccuracy(name="accuracy"),
            tf.keras.metrics.AUC(name="auc"),
            tf.keras.metrics.Precision(name="precision"),
            tf.keras.metrics.Recall(name="recall"),
        ],
    )


def configure_finetuning(model: tf.keras.Model) -> None:
    base_model = None
    for layer in model.layers:
        if isinstance(layer, tf.keras.Model) and layer.name.startswith("mobilenetv2"):
            base_model = layer
            break
    if base_model is None:
        raise RuntimeError("Could not locate MobileNetV2 base model for fine-tuning.")
    base_model.trainable = True
    for layer in base_model.layers[:FINE_TUNE_AT]:
        layer.trainable = False
    for layer in base_model.layers[FINE_TUNE_AT:]:
        if isinstance(layer, tf.keras.layers.BatchNormalization):
            layer.trainable = False


def collect_labels_and_probabilities(model: tf.keras.Model, dataset: tf.data.Dataset) -> tuple[np.ndarray, np.ndarray]:
    probabilities = model.predict(dataset, verbose=0).astype("float32").reshape(-1)
    labels = np.concatenate([batch_labels.numpy().reshape(-1) for _, batch_labels in dataset]).astype("int32")
    return labels, probabilities


def make_confusion_payload(labels: np.ndarray, probabilities: np.ndarray, threshold: float) -> dict:
    predictions = (probabilities >= threshold).astype("int32")
    matrix = confusion_matrix(labels, predictions, labels=[0, 1]).tolist()
    report = classification_report(
        labels,
        predictions,
        labels=[0, 1],
        target_names=CLASS_NAMES,
        output_dict=True,
        zero_division=0,
    )
    return {
        "threshold": threshold,
        "class_names": CLASS_NAMES,
        "matrix": matrix,
        "report": report,
    }


def evaluate_named_metrics(model: tf.keras.Model, dataset: tf.data.Dataset) -> dict:
    try:
        metrics = model.evaluate(dataset, verbose=0, return_dict=True)
        return {str(key): float(value) for key, value in metrics.items()}
    except TypeError:
        metrics = dict(zip(model.metrics_names, model.evaluate(dataset, verbose=0)))
        return {str(key): float(value) for key, value in metrics.items()}


def build_test_metrics(labels: np.ndarray, probabilities: np.ndarray, threshold: float) -> dict:
    predictions = (probabilities >= threshold).astype("int32")
    report = classification_report(
        labels,
        predictions,
        labels=[0, 1],
        target_names=CLASS_NAMES,
        output_dict=True,
        zero_division=0,
    )
    accuracy = float(np.mean(predictions == labels))
    auc = float(roc_auc_score(labels, probabilities))
    iris_metrics = report["iris_visible"]
    eyelid_metrics = report["eyelid_dominant"]
    return {
        "accuracy": accuracy,
        "binary_accuracy": accuracy,
        "auc": auc,
        "precision": float(iris_metrics["precision"]),
        "recall": float(iris_metrics["recall"]),
        "f1": float(iris_metrics["f1-score"]),
        "support": int(iris_metrics["support"]),
        "macro_precision": float(report["macro avg"]["precision"]),
        "macro_recall": float(report["macro avg"]["recall"]),
        "macro_f1": float(report["macro avg"]["f1-score"]),
        "eyelid_dominant_precision": float(eyelid_metrics["precision"]),
        "eyelid_dominant_recall": float(eyelid_metrics["recall"]),
        "eyelid_dominant_f1": float(eyelid_metrics["f1-score"]),
    }


def metric_value(metrics: dict, *candidate_names: str) -> float | None:
    for candidate_name in candidate_names:
        if candidate_name in metrics:
            return float(metrics[candidate_name])
    return None


def format_metric(metrics: dict, *candidate_names: str) -> str:
    value = metric_value(metrics, *candidate_names)
    return f"{value:.4f}" if value is not None else "n/a"


def plot_confusion_matrix(confusion_payload: dict, output_path: Path) -> None:
    matrix = np.array(confusion_payload["matrix"])
    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(matrix, cmap="Blues")
    ax.set_xticks(range(len(CLASS_NAMES)))
    ax.set_yticks(range(len(CLASS_NAMES)))
    ax.set_xticklabels(CLASS_NAMES, rotation=20, ha="right")
    ax.set_yticklabels(CLASS_NAMES)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title("Anterior View Router Confusion Matrix (test)")
    for row in range(matrix.shape[0]):
        for col in range(matrix.shape[1]):
            ax.text(col, row, str(matrix[row, col]), ha="center", va="center", color="black")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def build_runtime_fallback(probability_of_iris_visible: float) -> dict:
    if probability_of_iris_visible >= IRIS_VISIBLE_MIN_PROBABILITY:
        return {
            "decision_status": "confident_route",
            "predicted_label": "iris_visible",
            "recommended_route": "broad_anterior_screening",
        }
    if probability_of_iris_visible <= EYELID_DOMINANT_MAX_PROBABILITY:
        return {
            "decision_status": "confident_route",
            "predicted_label": "eyelid_dominant",
            "recommended_route": "eyelid_limited_screening",
        }
    return {
        "decision_status": "low_confidence_fallback",
        "predicted_label": None,
        "recommended_route": "manual_review_or_recapture",
        "fallback_reason": FALLBACK_REASON,
    }


def write_handoff(output_dir: Path, metrics_payload: dict) -> None:
    test_metrics = metrics_payload["test_metrics"]
    handoff = f"""# Anterior View Router V1 Binary Colab

Run name: `{RUN_NAME}`

Classes:

- eyelid_dominant
- iris_visible

Recommended runtime fallback:

- if `p(iris_visible) >= {IRIS_VISIBLE_MIN_PROBABILITY:.2f}` -> route as `iris_visible`
- if `p(iris_visible) <= {EYELID_DOMINANT_MAX_PROBABILITY:.2f}` -> route as `eyelid_dominant`
- otherwise -> `low_confidence_fallback`

Test metrics:

- accuracy: {format_metric(test_metrics, 'accuracy', 'binary_accuracy')}
- auc: {format_metric(test_metrics, 'auc')}
- precision: {format_metric(test_metrics, 'precision')}
- recall: {format_metric(test_metrics, 'recall')}

Artifacts:

- best_model.keras
- metrics.json
- confusion_matrix.json
- confusion_matrix.png
- label_map.json
- train_config.json
- inference_contract.json
- train_history.json
"""
    (output_dir / "HANDOFF.md").write_text(handoff, encoding="utf-8")


def main() -> None:
    seed_everything()
    enable_mixed_precision_if_gpu()
    mount_drive()

    drive_root = Path("/content/drive/MyDrive")
    dataset_zip = locate_dataset_zip(drive_root)
    extract_root = Path("/content/anterior_view_router_dataset")
    dataset_root = extract_dataset(dataset_zip, extract_root)

    train_dir = dataset_root / "splits" / "train"
    val_dir = dataset_root / "splits" / "val"
    test_dir = dataset_root / "splits" / "test"
    metadata_dir = dataset_root / "metadata"

    train_counts = count_dataset_files(train_dir)
    val_counts = count_dataset_files(val_dir)
    test_counts = count_dataset_files(test_dir)
    class_weights = build_class_weights(train_counts)

    train_ds = make_dataset(train_dir, training=True)
    val_ds = make_dataset(val_dir, training=False)
    test_ds = make_dataset(test_dir, training=False)

    autotune = tf.data.AUTOTUNE
    train_ds = train_ds.prefetch(autotune)
    val_ds = val_ds.prefetch(autotune)
    test_ds = test_ds.prefetch(autotune)

    output_dir = drive_root / "EyeScan_Models" / "Anterior_View_Router_V1_Binary"
    output_dir.mkdir(parents=True, exist_ok=True)
    best_model_path = output_dir / "best_model.keras"

    model = build_model()
    compile_model(model, INITIAL_LEARNING_RATE)

    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=EARLY_STOPPING_PATIENCE,
            restore_best_weights=True,
        ),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=str(best_model_path),
            monitor="val_accuracy",
            mode="max",
            save_best_only=True,
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=2,
            min_lr=1e-6,
        ),
    ]

    frozen_history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=FROZEN_EPOCHS,
        class_weight=class_weights,
        callbacks=callbacks,
        verbose=1,
    )

    configure_finetuning(model)
    compile_model(model, FINETUNE_LEARNING_RATE)
    finetune_history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=FROZEN_EPOCHS + FINETUNE_EPOCHS,
        initial_epoch=len(frozen_history.history["loss"]),
        class_weight=class_weights,
        callbacks=callbacks,
        verbose=1,
    )

    best_model = tf.keras.models.load_model(best_model_path, compile=False)
    compile_model(best_model, FINETUNE_LEARNING_RATE)
    sanitize_keras_archive(best_model_path)

    val_metrics = evaluate_named_metrics(best_model, val_ds)
    test_labels, test_probabilities = collect_labels_and_probabilities(best_model, test_ds)
    test_metrics = build_test_metrics(test_labels, test_probabilities, threshold=0.50)

    confusion_payload = make_confusion_payload(test_labels, test_probabilities, threshold=0.50)
    plot_confusion_matrix(confusion_payload, output_dir / "confusion_matrix.png")
    write_json(output_dir / "confusion_matrix.json", confusion_payload)

    label_map = {label: idx for idx, label in enumerate(CLASS_NAMES)}
    write_json(output_dir / "label_map.json", label_map)

    history_payload = {
        "frozen_stage": frozen_history.history,
        "finetune_stage": finetune_history.history,
    }
    write_json(output_dir / "train_history.json", history_payload)

    metrics_payload = {
        "run_name": RUN_NAME,
        "class_names": CLASS_NAMES,
        "dataset_zip": str(dataset_zip),
        "train_counts": train_counts,
        "val_counts": val_counts,
        "test_counts": test_counts,
        "class_weights": {CLASS_NAMES[idx]: weight for idx, weight in class_weights.items()},
        "val_metrics": {key: float(value) for key, value in val_metrics.items()},
        "test_metrics": {key: float(value) for key, value in test_metrics.items()},
        "runtime_fallback": {
            "iris_visible_min_probability": IRIS_VISIBLE_MIN_PROBABILITY,
            "eyelid_dominant_max_probability": EYELID_DOMINANT_MAX_PROBABILITY,
            "fallback_reason": FALLBACK_REASON,
        },
        "sample_runtime_decisions": {
            "p_iris_0.82": build_runtime_fallback(0.82),
            "p_iris_0.18": build_runtime_fallback(0.18),
            "p_iris_0.54": build_runtime_fallback(0.54),
        },
    }
    write_json(output_dir / "metrics.json", metrics_payload)

    train_config = {
        "run_name": RUN_NAME,
        "class_names": CLASS_NAMES,
        "image_size": list(IMAGE_SIZE),
        "batch_size": BATCH_SIZE,
        "frozen_epochs": FROZEN_EPOCHS,
        "finetune_epochs": FINETUNE_EPOCHS,
        "initial_learning_rate": INITIAL_LEARNING_RATE,
        "finetune_learning_rate": FINETUNE_LEARNING_RATE,
        "fine_tune_at": FINE_TUNE_AT,
        "augmentation": {
            "random_flip": "horizontal",
            "random_rotation": 0.03,
            "random_zoom": 0.05,
            "random_contrast": 0.10,
        },
        "class_balancing": {
            "strategy": "class_weight",
            "weights": {CLASS_NAMES[idx]: weight for idx, weight in class_weights.items()},
        },
        "split_counts": {
            "train": train_counts,
            "val": val_counts,
            "test": test_counts,
        },
    }
    write_json(output_dir / "train_config.json", train_config)

    inference_contract = {
        "task": "anterior_view_router_binary",
        "model_name": RUN_NAME,
        "input": {
            "color_mode": "RGB",
            "image_size": list(IMAGE_SIZE),
            "dtype": "float32",
            "preprocessing": "mobilenet_v2_preprocess_input",
        },
        "output": {
            "probabilities": {
                "eyelid_dominant": "1 - p(iris_visible)",
                "iris_visible": "sigmoid_output",
            },
            "hard_labels": CLASS_NAMES,
            "runtime_fallback": {
                "iris_visible_min_probability": IRIS_VISIBLE_MIN_PROBABILITY,
                "eyelid_dominant_max_probability": EYELID_DOMINANT_MAX_PROBABILITY,
                "fallback_status": "low_confidence_fallback",
                "fallback_reason": FALLBACK_REASON,
                "fallback_action": "do_not_hard_route_request_manual_review_or_recapture",
            },
        },
    }
    write_json(output_dir / "inference_contract.json", inference_contract)

    if metadata_dir.exists():
        shutil.copy2(metadata_dir / "anterior_view_router_v1_binary_manifest.jsonl", output_dir / "source_manifest.jsonl")
        if (metadata_dir / "export_summary.json").exists():
            shutil.copy2(metadata_dir / "export_summary.json", output_dir / "source_export_summary.json")

    write_handoff(output_dir, metrics_payload)

    package_dir = Path("/content") / f"{RUN_NAME}_package"
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir(parents=True, exist_ok=True)

    package_files = [
        "best_model.keras",
        "metrics.json",
        "confusion_matrix.json",
        "confusion_matrix.png",
        "label_map.json",
        "train_config.json",
        "inference_contract.json",
        "HANDOFF.md",
    ]
    for file_name in package_files:
        shutil.copy2(output_dir / file_name, package_dir / file_name)

    package_zip = output_dir / f"{RUN_NAME}_package.zip"
    if package_zip.exists():
        package_zip.unlink()
    shutil.make_archive(str(package_dir), "zip", root_dir=package_dir.parent, base_dir=package_dir.name)
    shutil.copy2(package_dir.parent / f"{package_dir.name}.zip", package_zip)

    print("Training complete.")
    print(f"Dataset zip: {dataset_zip}")
    print(f"Output directory: {output_dir}")
    print(f"Package zip: {package_zip}")


if __name__ == "__main__":
    main()
