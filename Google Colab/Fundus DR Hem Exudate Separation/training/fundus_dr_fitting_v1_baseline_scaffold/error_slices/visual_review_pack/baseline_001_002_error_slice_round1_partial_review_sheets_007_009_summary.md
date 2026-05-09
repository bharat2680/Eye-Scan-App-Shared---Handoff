# Round 1 Partial Review Support: Sheets 007-009

## Scope

This file summarizes the partial Round 1 review-support decisions for `errslice_007` through `errslice_009` only.
It is review-support documentation only. It does not relabel automatically and does not update any canonical manifest.

## Sheets Covered

- `contact_sheets/errslice_007.jpg`
- `contact_sheets/errslice_008.jpg`
- `contact_sheets/errslice_009.jpg`

## Row Counts By Decision Bucket

- `keep_label_model_wrong`: 14
- `relabel_to_predicted`: 3
- `downgrade_needs_second_review`: 28
- `unusable_low_quality`: 3
- Total partial review rows: 48

## Visual Boundary Note

Sheets 007-009 repeat the same pattern seen earlier: subtle DR misses, exudate rows overcalled as mixed, and several low-contrast or ambiguous rows needing second review.

## Counts By Sheet

### `contact_sheets/errslice_007.jpg`

- `keep_label_model_wrong`: 6
- `relabel_to_predicted`: 3
- `downgrade_needs_second_review`: 6
- `unusable_low_quality`: 1
- Total: 16

### `contact_sheets/errslice_008.jpg`

- `keep_label_model_wrong`: 4
- `relabel_to_predicted`: 0
- `downgrade_needs_second_review`: 10
- `unusable_low_quality`: 2
- Total: 16

### `contact_sheets/errslice_009.jpg`

- `keep_label_model_wrong`: 4
- `relabel_to_predicted`: 0
- `downgrade_needs_second_review`: 12
- `unusable_low_quality`: 0
- Total: 16

## Unmatched Or Unassigned Rows

- Unmatched supplied IDs: 0
- In-scope rows without a supplied decision: 0

## Guardrails

- Review-support only; no automatic label promotion or relabeling.
- `reviewed_manifest_v1.csv` was not modified.
- `fitting_manifest_v1.csv` was not modified.
- `challenge_manifest_v1.csv` was not created.
- No training, fitting execution, model export, TFLite export, app integration, or runtime/model-loading changes were made.

## Git Diff Summary

Expected diff for this task: two new review-support files only:

- `baseline_001_002_error_slice_round1_partial_review_sheets_007_009.csv`
- `baseline_001_002_error_slice_round1_partial_review_sheets_007_009_summary.md`
