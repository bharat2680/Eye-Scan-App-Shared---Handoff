# Google Colab Anterior View Router (Binary)

This folder contains the canonical Colab training path for the finalized
2-class anterior view router.

Trainable labels:

- `iris_visible`
- `eyelid_dominant`

Not trainable in this pass:

- `unclear`

Instead of training an `unclear` class, the runtime contract uses a
low-confidence fallback band.

## Source of truth

Reviewed labels:

- `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/datasets/anterior/view_router/labels_reviewed_final.csv`

Binary export spec:

- `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/configs/anterior_view_router_v1_binary_colab_export_spec.json`

Local export script:

- `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/scripts/export_anterior_view_router_binary_colab_dataset.py`

## Local export command

Run this on the Mac before uploading to Drive:

```bash
python3 /Users/bharatsharma/Documents/Playground/EyeScan_Shared/scripts/export_anterior_view_router_binary_colab_dataset.py \
  --spec /Users/bharatsharma/Documents/Playground/EyeScan_Shared/configs/anterior_view_router_v1_binary_colab_export_spec.json
```

This creates:

- dataset folder:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/datasets/anterior/view_router/colab_binary_v1/anterior_view_router_v1_binary_colab_dataset/`
- packaged zip:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/datasets/anterior/view_router/colab_binary_v1/anterior_view_router_v1_binary_colab_dataset.zip`

Export layout:

- `metadata/anterior_view_router_v1_binary_manifest.jsonl`
- `metadata/label_map.json`
- `metadata/export_summary.json`
- `splits/train/eyelid_dominant/`
- `splits/train/iris_visible/`
- `splits/val/...`
- `splits/test/...`

## Current split details

Using the finalized reviewed labels and deterministic split hashing:

- train:
  - `eyelid_dominant`: 175
  - `iris_visible`: 1247
- val:
  - `eyelid_dominant`: 31
  - `iris_visible`: 268
- test:
  - `eyelid_dominant`: 37
  - `iris_visible`: 284

Total included:

- `eyelid_dominant`: 243
- `iris_visible`: 1799

## Recommended Google Drive input

Upload the exported zip to one of these Drive locations:

- `MyDrive/EyeScan_Models/Colab_Datasets/anterior_view_router_v1_binary_colab_dataset.zip`
- `MyDrive/EyeScan_Models/colab_datasets/anterior_view_router_v1_binary_colab_dataset.zip`
- `MyDrive/Datasets/anterior_view_router_v1_binary_colab_dataset.zip`

The trainer looks for those paths in that order.

## Canonical Colab trainer

Training entry script:

- `train_anterior_view_router_v1_binary_colab.py`

Dependencies:

- `requirements_colab.txt`

Recommended Colab runtime:

1. Open Colab
2. Upload or paste `train_anterior_view_router_v1_binary_colab.py`
3. Switch runtime to `T4 GPU` if available
4. Run top-to-bottom

## Model / training defaults

- backbone: `MobileNetV2`
- image size: `224 x 224`
- batch size: `32`
- frozen stage: `5` epochs
- fine-tune stage: `8` epochs
- deterministic seed: `42`

## Class balancing strategy

This dataset is imbalanced:

- `iris_visible`: 1799
- `eyelid_dominant`: 243

Canonical balancing strategy:

- keep the dataset as-is
- apply `class_weight` during training based on train split counts
- keep augmentation symmetric and mild
- avoid synthetic oversampling first, so routing remains easy to interpret

Why this is preferred:

- reproducible
- lightweight
- avoids inventing new eyelid views artificially
- easy to compare with future router reruns

## Runtime fallback behavior

Because `unclear` is not trained as a third class in this pass, the runtime
should not hard-route every binary prediction.

Recommended behavior:

- if `p(iris_visible) >= 0.65` -> route as `iris_visible`
- if `p(iris_visible) <= 0.35` -> route as `eyelid_dominant`
- otherwise -> return `low_confidence_fallback`

Suggested fallback meaning:

- do not push the image into the conjunctivitis / uveitis / pterygium path
- request recapture or manual review
- keep this as a router safety guard, not as a disease output

## Planned output package

When the Colab run completes, it should produce:

- `best_model.keras`
- `metrics.json`
- `confusion_matrix.json`
- `confusion_matrix.png`
- `label_map.json`
- `train_config.json`
- `inference_contract.json`
- `HANDOFF.md`
- packaged zip:
  - `anterior_view_router_v1_mobilenetv2_binary_colab_package.zip`

Expected output directory on Drive:

- `MyDrive/EyeScan_Models/Anterior_View_Router_V1_Binary/`

## Packaging expectations

The training script already writes the packaging artifacts and assembles a
clean package zip after the run. No live app integration is part of this lane.
