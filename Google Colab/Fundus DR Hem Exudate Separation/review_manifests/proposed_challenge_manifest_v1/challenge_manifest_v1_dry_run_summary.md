# Challenge Manifest v1 Dry Run Summary

## Scope

This package creates `challenge_manifest_v1_dry_run.csv` only. It is an evaluation/stress-test planning artifact, not a canonical challenge manifest and not training data.

## Inputs

- Round 1 combined review-support rows considered: 197
- Proposed corrections rows used for validation: 50
- Proposed exclusion/review-hold rows used for validation: 90
- Proposed unassigned hold rows used for validation: 1
- Baseline 003 prediction overlap rows in dry run: 17

## Construction

- Included `keep_label_model_wrong` rows as hard model-error cases.
- Included `downgrade_needs_second_review` rows as boundary/uncertainty cases.
- Included `unusable_low_quality` rows only as quality stress cases.
- Included unassigned rows as review-hold challenge candidates.
- Included `relabel_to_predicted` rows as label-boundary correction candidates.
- Deduplicated by `evidence_id + challenge_category`.

## Counts

- Source rows considered: 197
- Final dry-run rows: 128
- Duplicate source rows removed: 69

### Source Rows By Review Action

- `downgrade_needs_second_review`: 81
- `keep_label_model_wrong`: 56
- `relabel_to_predicted`: 50
- `unassigned`: 1
- `unusable_low_quality`: 9

### Final Rows By Challenge Category

- `subtle_dr_missed_as_normal`: 5
- `exudate_vs_mixed_boundary`: 12
- `mixed_vs_dr_boundary`: 12
- `mixed_vs_exudate_boundary`: 7
- `low_quality_or_low_contrast`: 6
- `model_disagreement`: 1
- `needs_second_review_boundary`: 50
- `label_boundary_correction_candidate`: 35

### Final Rows By Review Action

- `downgrade_needs_second_review`: 50
- `keep_label_model_wrong`: 36
- `relabel_to_predicted`: 35
- `unassigned`: 1
- `unusable_low_quality`: 6

### Final Rows By Expected Handling

- `flag_for_second_review_not_training`: 50
- `label_boundary_candidate_requires_review`: 35
- `model_should_match_original_review_bucket`: 36
- `quality_stress_case_not_disease_truth`: 6
- `review_hold_before_canonical_use`: 1

## Warnings

- `challenge_manifest_v1.csv` was not created.
- This dry run is evaluation-only and must not be used for training.
- Quality and unusable rows are quality/exclusion stress cases, not disease-truth labels.
- Ambiguous and needs-second-review rows are not accepted disease truth.
- Do not mix these rows into `fitting_manifest_v1.csv` or `fitting_manifest_v2.csv`.

## Recommendation

Review `challenge_manifest_v1_dry_run.csv` manually before creating canonical `challenge_manifest_v1.csv`. Keep the first canonical challenge set small, traceable, and explicitly separate from training/fitting manifests.

## Guardrails

- No training or fitting execution was performed.
- No model files, weights, or TFLite exports were created.
- No app/backend/runtime/model-loading files were changed.
- `reviewed_manifest_v1.csv` was not modified.
- `fitting_manifest_v1.csv` was not modified.
- `fitting_manifest_v2.csv` was not modified.
- Canonical `challenge_manifest_v1.csv` remains absent.
