# Round 1 Partial Review Support: Sheets 010-013

## Scope

This file summarizes the partial Round 1 review-support decisions for `errslice_010` through `errslice_013` only.
It is review-support documentation only. It does not relabel automatically and does not update any canonical manifest.

## Sheets Covered

- `contact_sheets/errslice_010.jpg`
- `contact_sheets/errslice_011.jpg`
- `contact_sheets/errslice_012.jpg`
- `contact_sheets/errslice_013.jpg`

## Row Counts By Decision Bucket

- `keep_label_model_wrong`: 10
- `relabel_to_predicted`: 29
- `downgrade_needs_second_review`: 11
- `unusable_low_quality`: 3
- `unassigned_no_supplied_decision`: 0
- Total partial review rows: 53

## Unmatched Or Unassigned Rows

- Unmatched supplied IDs: 0
- In-scope rows without a supplied decision: 0

## Visual Boundary Note

Sheets 010-013 strongly reinforce that `mixed_hemorrhage_exudate_pattern` is over-broad and often overlaps visually with `dr_pattern_dominant` or `exudate_macular_pattern_dominant`. These rows should remain review-support evidence until a separate manual correction proposal is created and checked.

## Counts By Sheet

### `contact_sheets/errslice_010.jpg`

- `keep_label_model_wrong`: 4
- `relabel_to_predicted`: 8
- `downgrade_needs_second_review`: 4
- `unusable_low_quality`: 0
- `unassigned_no_supplied_decision`: 0
- Total: 16

### `contact_sheets/errslice_011.jpg`

- `keep_label_model_wrong`: 2
- `relabel_to_predicted`: 8
- `downgrade_needs_second_review`: 4
- `unusable_low_quality`: 2
- `unassigned_no_supplied_decision`: 0
- Total: 16

### `contact_sheets/errslice_012.jpg`

- `keep_label_model_wrong`: 3
- `relabel_to_predicted`: 10
- `downgrade_needs_second_review`: 2
- `unusable_low_quality`: 1
- `unassigned_no_supplied_decision`: 0
- Total: 16

### `contact_sheets/errslice_013.jpg`

- `keep_label_model_wrong`: 1
- `relabel_to_predicted`: 3
- `downgrade_needs_second_review`: 1
- `unusable_low_quality`: 0
- `unassigned_no_supplied_decision`: 0
- Total: 5

## Guardrails

- Review-support only; no automatic label promotion or relabeling.
- `reviewed_manifest_v1.csv` was not modified.
- `fitting_manifest_v1.csv` was not modified.
- `challenge_manifest_v1.csv` was not created.
- No training, fitting execution, model export, TFLite export, app integration, or runtime/model-loading changes were made.

## Git Diff Summary

Expected diff for this task: two new review-support files only:

- `baseline_001_002_error_slice_round1_partial_review_sheets_010_013.csv`
- `baseline_001_002_error_slice_round1_partial_review_sheets_010_013_summary.md`
