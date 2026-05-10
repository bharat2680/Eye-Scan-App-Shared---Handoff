# Challenge Manifest v1 Dry Run No-Train-Overlap Summary

## Scope

This package revises `challenge_manifest_v1_dry_run.csv` by excluding any row whose `evidence_id` appears in `fitting_manifest_v2.csv` with `train` split.
It is still a proposed dry-run artifact only. Canonical `challenge_manifest_v1.csv` is not created.

## Construction

- Original dry-run rows: 128
- Fitting v2 train-overlap unique evidence IDs removed: 32
- Fitting v2 train-overlap dry-run rows removed: 38
- Revised dry-run row count: 90
- Remaining fitting v2 train overlap rows: 0

The original readiness audit reported 32 overlapping train evidence IDs. Removing by evidence ID removes 38 dry-run rows because several evidence IDs had more than one challenge category.

## Remaining Fitting v2 Overlap

- Remaining fitting v2 `val` overlap unique evidence IDs: 7
- Remaining fitting v2 `val` overlap dry-run rows: 8
- Remaining fitting v2 `test` overlap unique evidence IDs: 9
- Remaining fitting v2 `test` overlap dry-run rows: 9

Rows overlapping only validation or test are preserved in this revised dry-run, but they remain evaluation-only challenge candidates and must not be mixed into training.

## Revised Rows By Challenge Category

- `exudate_vs_mixed_boundary`: 1
- `label_boundary_correction_candidate`: 23
- `low_quality_or_low_contrast`: 6
- `mixed_vs_dr_boundary`: 4
- `mixed_vs_exudate_boundary`: 1
- `model_disagreement`: 1
- `needs_second_review_boundary`: 50
- `subtle_dr_missed_as_normal`: 4

## Revised Rows By Review Action

- `downgrade_needs_second_review`: 50
- `keep_label_model_wrong`: 10
- `relabel_to_predicted`: 23
- `unassigned`: 1
- `unusable_low_quality`: 6

## Revised Rows By Expected Handling

- `flag_for_second_review_not_training`: 50
- `label_boundary_candidate_requires_review`: 23
- `model_should_match_original_review_bucket`: 10
- `quality_stress_case_not_disease_truth`: 6
- `review_hold_before_canonical_use`: 1

## Removed Rows By Challenge Category

- `exudate_vs_mixed_boundary`: 11
- `label_boundary_correction_candidate`: 12
- `mixed_vs_dr_boundary`: 8
- `mixed_vs_exudate_boundary`: 6
- `subtle_dr_missed_as_normal`: 1

## Removed Rows By Review Action

- `keep_label_model_wrong`: 26
- `relabel_to_predicted`: 12

## Readiness Recommendation

This revised dry-run is now eligible for canonical challenge-manifest review from a no-train-overlap perspective because it has zero overlap with `fitting_manifest_v2.csv` train evidence IDs.
Before creating canonical `challenge_manifest_v1.csv`, still review whether preserved validation/test overlaps are acceptable for the intended evaluation protocol, and confirm challenge rows remain separate from any future fitting manifests.

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
