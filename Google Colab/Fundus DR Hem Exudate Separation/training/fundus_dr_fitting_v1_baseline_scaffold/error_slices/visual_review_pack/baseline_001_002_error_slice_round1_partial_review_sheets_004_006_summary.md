# Round 1 Partial Review Support: Sheets 004-006

## Scope

This file summarizes the partial Round 1 review-support decisions for `errslice_004` through `errslice_006` only.
It is review-support documentation only. It does not relabel automatically and does not update any canonical manifest.

## Sheets Covered

- `contact_sheets/errslice_004.jpg`
- `contact_sheets/errslice_005.jpg`
- `contact_sheets/errslice_006.jpg`

## Row Counts By Decision Bucket

- `keep_label_model_wrong`: 16
- `relabel_to_predicted`: 18
- `downgrade_needs_second_review`: 13
- `unassigned_no_supplied_decision`: 1
- Total partial review rows: 48

## Decision Coverage Note

The supplied decision list included `large_dr_b001_mixed_000464`, but that evidence ID is not on sheets 004-006. It appears elsewhere in the review template, so it was not applied in this scoped partial file.

Observed locations for the out-of-scope supplied ID:

- `large_dr_b001_mixed_000464 -> contact_sheets/errslice_007.jpg r2c1`
- `large_dr_b001_mixed_000464 -> contact_sheets/errslice_013.jpg r2c1`

Rows on sheets 004-006 without a supplied decision were left blank:

- `large_dr_b001_mixed_000400`

## Visual Boundary Note

Sheets 004-006 show that `mixed_hemorrhage_exudate_pattern` is too broad and often overlaps visually with `dr_pattern_dominant` or `exudate_macular_pattern_dominant`. These rows should remain review-support evidence until a separate manual correction proposal is created and checked.

## Counts By Sheet

### `contact_sheets/errslice_004.jpg`

- `keep_label_model_wrong`: 7
- `relabel_to_predicted`: 3
- `downgrade_needs_second_review`: 6
- `unassigned_no_supplied_decision`: 0
- Total: 16

### `contact_sheets/errslice_005.jpg`

- `keep_label_model_wrong`: 4
- `relabel_to_predicted`: 6
- `downgrade_needs_second_review`: 5
- `unassigned_no_supplied_decision`: 1
- Total: 16

### `contact_sheets/errslice_006.jpg`

- `keep_label_model_wrong`: 5
- `relabel_to_predicted`: 9
- `downgrade_needs_second_review`: 2
- `unassigned_no_supplied_decision`: 0
- Total: 16

## Guardrails

- Review-support only; no automatic label promotion or relabeling.
- `reviewed_manifest_v1.csv` was not modified.
- `fitting_manifest_v1.csv` was not modified.
- `challenge_manifest_v1.csv` was not created.
- No training, fitting execution, model export, TFLite export, app integration, or runtime/model-loading changes were made.

## Git Diff Summary

Expected diff for this task: two new review-support files only:

- `baseline_001_002_error_slice_round1_partial_review_sheets_004_006.csv`
- `baseline_001_002_error_slice_round1_partial_review_sheets_004_006_summary.md`
