# Baseline 001/002 Round 1 Proposed Corrections Summary

## Warning

This is a proposal-only package. It does not apply corrections to `reviewed_manifest_v1.csv`, `fitting_manifest_v1.csv`, or any other canonical manifest.
It does not run training, fitting execution, model export, TFLite export, app integration, model promotion, or production evaluation.

## Inputs

- Source review support: `../visual_review_pack/baseline_001_002_error_slice_round1_combined_review_support.csv`
- Total Round 1 rows: 197

## Output Files

- `baseline_001_002_round1_proposed_corrections.csv`
- `baseline_001_002_round1_proposed_exclusions.csv`
- `baseline_001_002_round1_unassigned_review_hold.csv`

## Counts By Review Action

- `keep_label_model_wrong`: 56 (not included as correction candidates)
- `relabel_to_predicted`: 50 (proposed corrections)
- `downgrade_needs_second_review`: 81 (review-hold/exclusion file)
- `unusable_low_quality`: 9 (proposed exclusions)
- `unassigned`: 1 (separate hold, no proposed action)

## Package Counts

- Proposed correction rows: 50
- Needs-second-review hold rows: 81
- Unusable-low-quality exclusion rows: 9
- Total proposed exclusions/review-hold rows: 90
- Unassigned review-hold rows: 1

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

## Interpretation

The Round 1 support package suggests that `mixed_hemorrhage_exudate_pattern` remains over-broad and often overlaps visually with `dr_pattern_dominant` or `exudate_macular_pattern_dominant`. Some exudate rows remain ambiguous or low contrast, and many DR-to-normal errors appear to be subtle DR misses rather than truly normal examples.

## Recommendation

- Inspect proposed corrections before touching `reviewed_manifest_v1.csv` or `fitting_manifest_v1.csv`.
- Keep `downgrade_needs_second_review` and unassigned rows out of automatic correction flows until reviewed again.
- Treat `unusable_low_quality` rows as proposed exclusions only, pending review.
- Do not run Baseline 003 until this correction package is reviewed and any manifest edits are separately proposed and verified.

## Guardrails

- No canonical manifest changes were made.
- `challenge_manifest_v1.csv` was not created.
- No training, fitting execution, model export, TFLite export, app integration, or model promotion was performed.
- No app/backend/runtime/model-loading files were changed.

## Git Diff Summary

Expected diff for this task: five new proposal-package files only in `round1_proposed_corrections/`.
