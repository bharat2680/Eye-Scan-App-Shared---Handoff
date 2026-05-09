# Round 1 Partial Review Support: Sheets 001-003

## Scope

This file summarizes the partial Round 1 review-support decisions for `errslice_001` through `errslice_003` only.
It is review-support documentation only. It does not relabel automatically and does not update any manifest.

## Sheets Covered

- `contact_sheets/errslice_001.jpg`
- `contact_sheets/errslice_002.jpg`
- `contact_sheets/errslice_003.jpg`

## Row Counts By Decision Bucket

- `keep_label_model_wrong`: 16
- `downgrade_needs_second_review`: 29
- `unusable_low_quality`: 3
- Total partial review rows: 48

The user-provided `needs_second_review` suggestions were stored as `downgrade_needs_second_review` to match the allowed Round 1 review action vocabulary.

## Counts By Sheet

### `contact_sheets/errslice_001.jpg`

- `keep_label_model_wrong`: 8
- `downgrade_needs_second_review`: 7
- `unusable_low_quality`: 1
- Total: 16

### `contact_sheets/errslice_002.jpg`

- `keep_label_model_wrong`: 3
- `downgrade_needs_second_review`: 11
- `unusable_low_quality`: 2
- Total: 16

### `contact_sheets/errslice_003.jpg`

- `keep_label_model_wrong`: 5
- `downgrade_needs_second_review`: 11
- `unusable_low_quality`: 0
- Total: 16

## Guardrails

- Review-support only; no automatic label promotion or relabeling.
- `reviewed_manifest_v1.csv` was not modified.
- `fitting_manifest_v1.csv` was not modified.
- `challenge_manifest_v1.csv` was not created.
- No training, fitting execution, model export, TFLite export, app integration, or runtime/model-loading changes were made.

## Git Diff Summary

Expected diff for this task: two new review-support files only:

- `baseline_001_002_error_slice_round1_partial_review_sheets_001_003.csv`
- `baseline_001_002_error_slice_round1_partial_review_sheets_001_003_summary.md`
