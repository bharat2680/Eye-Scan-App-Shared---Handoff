# Challenge Manifest v1 Independent Dry Run Summary

## Scope

This package creates `challenge_manifest_v1_dry_run_independent.csv` by removing every row from the no-train-overlap dry-run whose `evidence_id` appears anywhere in `fitting_manifest_v2.csv`.
It is still a proposed dry-run artifact only. Canonical `challenge_manifest_v1.csv` is not created.

## Construction

- Starting no-train-overlap rows: 90
- Fitting v2 train-overlap rows removed from this step: 0
- Fitting v2 val-overlap rows removed: 8
- Fitting v2 test-overlap rows removed: 9
- Total fitting v2 overlap rows removed: 17
- Total fitting v2 overlap unique evidence IDs removed: 16
- Final independent dry-run row count: 73
- Remaining overlap with fitting v2: 0

The previous no-train-overlap dry-run had already removed train overlap. This independent dry-run removes the remaining validation/test overlap as well.

## Independent Rows By Challenge Category

- `label_boundary_correction_candidate`: 13
- `low_quality_or_low_contrast`: 6
- `mixed_vs_dr_boundary`: 1
- `mixed_vs_exudate_boundary`: 1
- `model_disagreement`: 1
- `needs_second_review_boundary`: 50
- `subtle_dr_missed_as_normal`: 1

## Independent Rows By Review Action

- `downgrade_needs_second_review`: 50
- `keep_label_model_wrong`: 3
- `relabel_to_predicted`: 13
- `unassigned`: 1
- `unusable_low_quality`: 6

## Independent Rows By Expected Handling

- `flag_for_second_review_not_training`: 50
- `label_boundary_candidate_requires_review`: 13
- `model_should_match_original_review_bucket`: 3
- `quality_stress_case_not_disease_truth`: 6
- `review_hold_before_canonical_use`: 1

## Removed Rows By Challenge Category

- `exudate_vs_mixed_boundary`: 1
- `label_boundary_correction_candidate`: 10
- `mixed_vs_dr_boundary`: 3
- `subtle_dr_missed_as_normal`: 3

## Removed Rows By Review Action

- `keep_label_model_wrong`: 7
- `relabel_to_predicted`: 10

## Readiness Recommendation

This independent dry-run is eligible for canonical challenge-manifest review from a fitting v2 independence perspective because it has zero evidence-ID overlap with `fitting_manifest_v2.csv` across train, val, and test splits.
Before creating canonical `challenge_manifest_v1.csv`, review whether 73 rows is sufficient coverage for the intended stress-test slices and confirm the challenge set remains separate from future fitting manifests.

## Warnings

- This is evaluation-only challenge planning data, not training data.
- Canonical `challenge_manifest_v1.csv` was not created.
- Do not use challenge rows for fitting or training.
- Do not integrate this into app/backend/runtime.
- Do not promote any model based on this dry-run alone.

## Guardrails

- No training or fitting execution was performed.
- No model files, weights, or TFLite exports were created.
- No app/backend/runtime/model-loading files were changed.
- `reviewed_manifest_v1.csv` was not modified.
- `fitting_manifest_v1.csv` was not modified.
- `fitting_manifest_v2.csv` was not modified.
- Canonical `challenge_manifest_v1.csv` remains absent.
