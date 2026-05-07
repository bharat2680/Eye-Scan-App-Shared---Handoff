# Fundus DR Fitting v1 Training Plan

## Objective

Establish a small baseline classification experiment for the approved fitting
manifest `fitting_manifest_v1.csv`.

This is an evaluation-only baseline lane. It is not a production training
approval and not an app-integration lane.

## Input Source Expectations

- Source manifest:
  `Google Colab/Fundus DR Hem Exudate Separation/review_manifests/fitting_manifest_v1.csv`
- The manifest contains four balanced reviewed classes and fixed split
  assignments.
- Training runtime must resolve external image paths safely; raw images are not
  committed to the repository.

## Class Labels

- `normal_or_non_specific`
- `dr_pattern_dominant`
- `exudate_macular_pattern_dominant`
- `mixed_hemorrhage_exudate_pattern`

Suggested label index mapping:

- `0 = normal_or_non_specific`
- `1 = dr_pattern_dominant`
- `2 = exudate_macular_pattern_dominant`
- `3 = mixed_hemorrhage_exudate_pattern`

## Split Counts

- Total rows: 1864
- Per class: 466
- `train`: 1304
- `val`: 280
- `test`: 280

Per class split counts:

- `train`: 326
- `val`: 70
- `test`: 70

## Preprocessing Proposal

- Resolve each manifest `image_path` safely in the training runtime.
- Convert images to RGB if needed.
- Resize to a consistent input resolution, such as `224 x 224`.
- Normalize pixel values to the range expected by the chosen backbone.
- Preserve deterministic preprocessing between validation and test.

## Augmentation Proposal

Use light-to-moderate fundus-safe augmentation for training only:

- random horizontal flip if clinically acceptable for this lane
- mild rotation
- small zoom / crop jitter
- mild brightness / contrast jitter

Avoid aggressive augmentation that can distort lesion morphology or introduce
artificial artifacts.

## Baseline Architecture Proposal

Suggested baseline backbone options:

- `EfficientNetB0`
- `MobileNetV3Small`

Recommendation:

- start with `EfficientNetB0` as the first baseline
- use `MobileNetV3Small` only as a secondary lighter comparison if desired

## Metrics To Save

- accuracy
- macro F1
- per-class precision
- per-class recall
- per-class F1
- confusion matrix
- ROC / AUC only if the implementation is clean for a four-class setting

## Early Stopping Criteria

- monitor validation macro F1 or validation loss
- use patience, for example `5` to `8` epochs
- restore best validation weights for evaluation only

## Failure Criteria

Treat the baseline as failed or insufficient if:

- macro F1 is weak across multiple classes
- confusion matrix shows heavy collapse into one or two classes
- validation and test results diverge sharply
- data path resolution is inconsistent or brittle

## No-Promotion Criteria

Do not promote baseline results toward product or app integration if:

- only one backbone has been tried
- results are unstable across reruns
- class confusion remains high
- image path resolution is incomplete
- no error analysis or confusion-matrix review has been completed

This scaffold does not approve:

- production claims
- app/backend/runtime integration
- model export or deployment
