# Fundus DR Fitting v2 Baseline 003 Execution Plan

## Purpose

Baseline 003 is an evaluation-only experiment using the corrected and balanced `fitting_manifest_v2.csv`. Its purpose is to measure whether the Round 1 error-slice cleanup improves the four-class evidence classifier relative to Baseline 001 and Baseline 002.

This plan does not authorize app integration, model promotion, production claims, TFLite export, or changes to app/backend/runtime/model-loading files.

## Inputs

- Canonical v2 fitting manifest: `Google Colab/Fundus DR Hem Exudate Separation/review_manifests/fitting_manifest_v2.csv`
- Windows resolved manifest: `F:\EyeScan_Local_Data\large_dr_82gb_work\fitting_v2_resolved_manifest_windows.csv`

Verified v2 state:

- `fitting_manifest_v2.csv`: 1,696 rows
- Resolved image rows: 1,696
- Missing images: 0

## Class Mapping

- `0`: `normal_or_non_specific`
- `1`: `dr_pattern_dominant`
- `2`: `exudate_macular_pattern_dominant`
- `3`: `mixed_hemorrhage_exudate_pattern`

## Split Counts

Overall split counts:

- `train`: 1,184
- `val`: 256
- `test`: 256

Per-class split counts:

| Class | Train | Val | Test | Total |
| --- | ---: | ---: | ---: | ---: |
| `normal_or_non_specific` | 296 | 64 | 64 | 424 |
| `dr_pattern_dominant` | 296 | 64 | 64 | 424 |
| `exudate_macular_pattern_dominant` | 296 | 64 | 64 | 424 |
| `mixed_hemorrhage_exudate_pattern` | 296 | 64 | 64 | 424 |

## Recommended Baseline 003 Setup

Use the same simpler training setup as Baseline 001:

- EfficientNetB0
- ImageNet initialization
- Input size: 224 x 224
- Frozen backbone
- Train classifier head only
- Light train-only augmentation
- Deterministic validation/test preprocessing
- Early stopping on validation macro F1 or validation loss
- Restore best validation weights for final evaluation

Rationale: Baseline 003 should isolate the effect of the corrected/balanced v2 data. Do not use top-block fine-tuning in Baseline 003, because Baseline 002 showed that fine-tuning did not materially improve the main error boundaries.

## Metrics To Save

- Accuracy
- Macro F1
- Weighted F1
- Per-class precision
- Per-class recall
- Per-class F1
- Confusion matrix
- Strong confusion pairs
- Comparison against Baseline 001 and Baseline 002

## Output Location

Future external run folder:

`F:\EyeScan_Local_Data\large_dr_82gb_work\fitting_v1_training_runs\baseline_003_v2\`

If run later, commit only small summary artifacts such as metrics JSON/CSV, classification report, confusion matrix CSV, and a run summary markdown. Do not commit model weights, raw images, TFLite files, temporary runners, or virtual environments.

## Safety Rules

- Evaluation-only.
- No TFLite export.
- No app/backend/runtime integration.
- No production claims.
- No model promotion.
- No changes to `reviewed_manifest_v1.csv`.
- No changes to `fitting_manifest_v1.csv`.
- No changes to `fitting_manifest_v2.csv`.
- Do not create `challenge_manifest_v1.csv`.

## Readiness Checks Before Running Later

- Confirm `fitting_manifest_v2.csv` still has 1,696 rows.
- Confirm class counts are 424 each.
- Confirm split counts are `train` 1,184, `val` 256, `test` 256.
- Confirm `F:\EyeScan_Local_Data\large_dr_82gb_work\fitting_v2_resolved_manifest_windows.csv` exists and has 1,696 rows.
- Confirm all resolved image paths exist.
- Confirm no app/backend/runtime/model-loading files are modified before training.

## Current Verification

- `fitting_manifest_v2.csv`: 1,696 rows
- `fitting_manifest_v1.csv`: 1,864 rows
- `reviewed_manifest_v1.csv`: 2,955 rows
- `challenge_manifest_v1.csv`: absent
- No training/model/app/backend/runtime changes were made by this plan.

## Git Diff Summary

Expected diff for this task: this execution plan markdown only.
