# Fundus DR Fitting v1 Baseline Execution Plan

This document defines the final baseline execution plan for a future
evaluation-only training run of `fundus_dr_fitting_v1` on Dell/Windows.

It does not approve training in this task, does not create model files, and
does not authorize app, backend, runtime, or production integration.

## Exact Input Files

Use these two inputs together:

- canonical fitting manifest:
  `Google Colab/Fundus DR Hem Exudate Separation/review_manifests/fitting_manifest_v1.csv`
- Dell/Windows resolved manifest:
  `F:\EyeScan_Local_Data\large_dr_82gb_work\fitting_v1_resolved_manifest_windows.csv`

The canonical fitting manifest defines labels and split assignments. The
resolved manifest provides the verified Dell/Windows external image paths for
all rows.

## Four-Class Label Mapping

- `0 = normal_or_non_specific`
- `1 = dr_pattern_dominant`
- `2 = exudate_macular_pattern_dominant`
- `3 = mixed_hemorrhage_exudate_pattern`

## Split Counts

- total rows: `1864`
- `train`: `1304`
- `val`: `280`
- `test`: `280`

Resolved image availability already verified on Dell:

- total resolved rows: `1864`
- Large DR resolved rows: `1766`
- Batch 008 resolved rows: `98`

## Recommended First Baseline

Use this as the first baseline configuration:

- backbone: `EfficientNetB0`
- image size: `224 x 224`
- train augmentation: light augmentation only
- validation and test preprocessing: deterministic only
- early stopping: monitor validation macro F1 or validation loss

Recommended light train-only augmentation:

- mild horizontal flip if the training implementation keeps laterality handling
  explicit
- small rotation
- small zoom / crop jitter
- mild brightness / contrast jitter

Avoid aggressive augmentation that can distort lesions, exudates, or
hemorrhage patterns.

## Metrics To Save

For the first baseline run, save at minimum:

- accuracy
- macro F1
- per-class precision
- per-class recall
- per-class F1
- confusion matrix

## Future Training Output Folder

If a later approved training run is started, write outputs only under:

- `F:\EyeScan_Local_Data\large_dr_82gb_work\fitting_v1_training_runs\baseline_001\`

That future run folder should hold only run-local artifacts such as logs,
checkpoints, metrics, and plots. It should not write raw image copies into the
repository.

## Execution Sequence For A Future Run

1. Validate `fitting_manifest_v1.csv`.
2. Resolve and verify all image paths from
   `fitting_v1_resolved_manifest_windows.csv`.
3. Build the four-class dataset using the fixed split assignments already in the
   manifest.
4. Train only on `train`, use `val` for early stopping and model selection, and
   reserve `test` for final evaluation-only reporting.
5. Save the required metrics and confusion matrix.
6. Review class-wise failures before considering any follow-up experiment.

## Explicit No-Promotion Rule

The first baseline run is evaluation-only.

- no app/backend integration
- no model promotion
- no production claims

Any later decision to continue beyond baseline must be based on a separate
review of data quality, training stability, and class-level failure patterns.

## Failure Criteria

Treat the first baseline as failed or insufficient if any of the following are
observed:

- class collapse
- severe confusion between DR, exudate, and mixed classes
- unstable validation/test gap
- missing image path resolution

Additional caution signs:

- strong dependence on one metric while macro F1 remains weak
- poor per-class recall in `dr_pattern_dominant`,
  `exudate_macular_pattern_dominant`, or
  `mixed_hemorrhage_exudate_pattern`
- brittle rerun behavior once training is eventually attempted

## Scope Guardrails

- no training is performed by this planning document
- no fitting is performed by this planning document
- no model files are created here
- no TFLite export is created here
- no app/backend/runtime/model files are changed here
- `reviewed_manifest_v1.csv` is not to be modified
- `fitting_manifest_v1.csv` is not to be modified
- `challenge_manifest_v1.csv` remains absent
