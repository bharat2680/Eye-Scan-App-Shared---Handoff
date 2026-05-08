# Baseline 001/002 Prediction Export Audit

This audit records the inference-only per-row prediction export used to populate
the Baseline 001/002 error-slice review index.

No training, fitting execution, app/backend/runtime integration, TFLite export,
model promotion, manifest edit, or raw image copy was performed.

## Checkpoint Availability

Both external evaluation checkpoints were present on Dell/Windows:

- Baseline 001:
  `F:\EyeScan_Local_Data\large_dr_82gb_work\fitting_v1_training_runs\baseline_001\best_model_state.pt`
- Baseline 002:
  `F:\EyeScan_Local_Data\large_dr_82gb_work\fitting_v1_training_runs\baseline_002\best_model_state.pt`

The checkpoints were used for inference-only prediction export on the existing
`val` and `test` splits.

## External Per-Row Prediction CSVs

Full per-row prediction CSVs were written outside the repository:

- Baseline 001:
  `F:\EyeScan_Local_Data\large_dr_82gb_work\fitting_v1_training_runs\baseline_001\baseline_001_per_row_predictions_val_test.csv`
- Baseline 002:
  `F:\EyeScan_Local_Data\large_dr_82gb_work\fitting_v1_training_runs\baseline_002\baseline_002_per_row_predictions_val_test.csv`

Each external CSV has `560` rows: `280` validation rows and `280` test rows.

## Repo-Side Summary Artifacts

Only small review summary artifacts are committed:

- `baseline_001_002_error_slice_index.csv`
- `baseline_001_002_prediction_export_summary.csv`

The populated error-slice index contains only the target review slices from
Baseline 001 and Baseline 002.

## Target Error-Slice Counts

| run | split | target error-slice rows |
| --- | --- | ---: |
| `baseline_001` | `val` | 49 |
| `baseline_001` | `test` | 52 |
| `baseline_002` | `val` | 43 |
| `baseline_002` | `test` | 53 |

Total target error-slice rows in the committed index: `197`.

## Future Baseline Requirement

Baseline 003 and later must save per-row prediction exports with:

- `evidence_id`
- `split`
- `image_path`
- true class
- predicted class
- confidence, logits, or probabilities
- source batch and source dataset

These prediction exports are required before any future error-slice review can
be made row-specific.

## Guardrails

- no model weights are committed
- no `.pth`, `.pt`, `.onnx`, or `.tflite` files are committed
- no raw images are committed
- no app/backend/runtime/model-loading files are changed
- `reviewed_manifest_v1.csv` is unchanged
- `fitting_manifest_v1.csv` is unchanged
- `challenge_manifest_v1.csv` remains absent
- temporary runner and environment files are not committed
