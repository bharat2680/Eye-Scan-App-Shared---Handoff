# Baseline 001/002 Round 1 Review Support Summary

## Scope

This package combines all partial Round 1 review-support files for the Baseline 001/002 error-slice visual review pack.
It is review-support documentation only. It does not apply label changes, update canonical manifests, run training, promote a model, or integrate anything into the app/runtime.

## Inputs Combined

- `baseline_001_002_error_slice_round1_partial_review_sheets_001_003.csv`: 48 rows
- `baseline_001_002_error_slice_round1_partial_review_sheets_004_006.csv`: 48 rows
- `baseline_001_002_error_slice_round1_partial_review_sheets_007_009.csv`: 48 rows
- `baseline_001_002_error_slice_round1_partial_review_sheets_010_013.csv`: 53 rows

## Combined Row Count

- Total combined rows: 197
- Duplicate `review_row_id` values: 0
- Duplicate full row identities: 0
- Repeated `evidence_id` values across baseline runs/contact sheets: 89

Repeated evidence IDs are expected where the same example appears as an error candidate in more than one baseline run or contact sheet. The combined file keeps those rows separate because the review row is run/contact-sheet specific.

## Rows By Review Action

- `keep_label_model_wrong`: 56
- `relabel_to_predicted`: 50
- `downgrade_needs_second_review`: 81
- `unusable_low_quality`: 9
- `unassigned`: 1

## Rows By Original True Class

- `dr_pattern_dominant`: 20
- `exudate_macular_pattern_dominant`: 80
- `mixed_hemorrhage_exudate_pattern`: 97

## Rows By Predicted Class

- `dr_pattern_dominant`: 66
- `exudate_macular_pattern_dominant`: 31
- `mixed_hemorrhage_exudate_pattern`: 80
- `normal_or_non_specific`: 20

## Rows By Error Slice

- `dr_pattern_dominant -> normal_or_non_specific`: 20
- `exudate_macular_pattern_dominant -> mixed_hemorrhage_exudate_pattern`: 80
- `mixed_hemorrhage_exudate_pattern -> dr_pattern_dominant`: 66
- `mixed_hemorrhage_exudate_pattern -> exudate_macular_pattern_dominant`: 31

## Rows By Contact Sheet

- `contact_sheets/errslice_001.jpg`: 16
- `contact_sheets/errslice_002.jpg`: 16
- `contact_sheets/errslice_003.jpg`: 16
- `contact_sheets/errslice_004.jpg`: 16
- `contact_sheets/errslice_005.jpg`: 16
- `contact_sheets/errslice_006.jpg`: 16
- `contact_sheets/errslice_007.jpg`: 16
- `contact_sheets/errslice_008.jpg`: 16
- `contact_sheets/errslice_009.jpg`: 16
- `contact_sheets/errslice_010.jpg`: 16
- `contact_sheets/errslice_011.jpg`: 16
- `contact_sheets/errslice_012.jpg`: 16
- `contact_sheets/errslice_013.jpg`: 5

## Major Pattern

Round 1 review support points to a label-boundary issue rather than a simple model tuning issue:

- `mixed_hemorrhage_exudate_pattern` appears over-broad.
- Many mixed rows overlap visually with `dr_pattern_dominant`.
- Some mixed rows overlap visually with `exudate_macular_pattern_dominant`.
- Some exudate rows are ambiguous, low contrast, or overcalled as mixed.
- Many `dr_pattern_dominant -> normal_or_non_specific` rows are subtle misses rather than truly normal images.

## Recommendation

- Create a proposed correction package only.
- Do not edit `reviewed_manifest_v1.csv` yet.
- Do not edit `fitting_manifest_v1.csv` yet.
- Do not create `challenge_manifest_v1.csv` yet.
- Do not run Baseline 003 until proposed corrections are reviewed.
- Do not promote either baseline model or export TFLite from these review-support notes.

## Guardrails Confirmed For This Package

- No training or fitting execution was performed.
- No model files, weights, TFLite exports, app/backend/runtime/model-loading files, or raw images were created or modified.
- `reviewed_manifest_v1.csv` was not modified.
- `fitting_manifest_v1.csv` was not modified.
- `challenge_manifest_v1.csv` was not created.

## Git Diff Summary

Expected diff for this task: two new combined review-support files only:

- `baseline_001_002_error_slice_round1_combined_review_support.csv`
- `BASELINE_001_002_ROUND1_REVIEW_SUPPORT_SUMMARY.md`
