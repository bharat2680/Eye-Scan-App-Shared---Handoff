# Error-Slice Visual Review Pack

This visual review pack supports manual error analysis for Baseline 001 and
Baseline 002 Fundus DR fitting v1 error slices.

This is visual error analysis only.

- It does not modify `reviewed_manifest_v1.csv`.
- It does not modify `fitting_manifest_v1.csv`.
- It does not create `challenge_manifest_v1.csv`.
- It does not train or integrate any model.
- It does not make diagnosis claims.
- It does not create accepted relabeling.

Rows may later become label-boundary correction proposals only after manual
visual review.

## Contents

- `baseline_001_002_error_slice_visual_review_index.csv`
- `contact_sheets/`

## Counts

- source error-slice rows: `197`
- visual review index rows: `197`
- missing resolved images: `0`
- contact sheets: `13`

## Manual Review Fields

Leave these fields blank until manual review:

- `review_action`
- `corrected_bucket`
- `notes`

Allowed `review_action` values:

- `keep_label_model_wrong`
- `relabel_to_predicted`
- `relabel_to_mixed`
- `downgrade_needs_second_review`
- `unusable_low_quality`
- `exclude_from_future_fitting`

## Review Scope

The target slices are:

- `exudate_macular_pattern_dominant -> mixed_hemorrhage_exudate_pattern`
- `mixed_hemorrhage_exudate_pattern -> dr_pattern_dominant`
- `mixed_hemorrhage_exudate_pattern -> exudate_macular_pattern_dominant`
- `dr_pattern_dominant -> normal_or_non_specific`
