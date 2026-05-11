# Challenge Manifest v1 Creation Summary

## Scope

`challenge_manifest_v1.csv` was created from the approved independent dry-run:

`proposed_challenge_manifest_v1/challenge_manifest_v1_dry_run_independent.csv`

This manifest is an evaluation/stress-test manifest only. It is not training data, not fitting data, not app/backend integration, not production approval, and not a model-promotion artifact.

## Creation Verification

- Rows copied from approved independent dry-run: 73
- Canonical `challenge_manifest_v1.csv` rows: 73
- Rows added or removed during creation: 0
- Schema and values preserved from the approved independent dry-run: yes
- Duplicate `challenge_id` values: 0
- Duplicate `evidence_id + challenge_category` pairs: 0
- `fitting_manifest_v2.csv` evidence-ID overlap: 0

## Challenge Category Counts

- `label_boundary_correction_candidate`: 13
- `low_quality_or_low_contrast`: 6
- `mixed_vs_dr_boundary`: 1
- `mixed_vs_exudate_boundary`: 1
- `model_disagreement`: 1
- `needs_second_review_boundary`: 50
- `subtle_dr_missed_as_normal`: 1

## Review Action Counts

- `downgrade_needs_second_review`: 50
- `keep_label_model_wrong`: 3
- `relabel_to_predicted`: 13
- `unassigned`: 1
- `unusable_low_quality`: 6

## Expected Handling Counts

- `flag_for_second_review_not_training`: 50
- `label_boundary_candidate_requires_review`: 13
- `model_should_match_original_review_bucket`: 3
- `quality_stress_case_not_disease_truth`: 6
- `review_hold_before_canonical_use`: 1

## Interpretation

The canonical challenge manifest is smaller but independent from `fitting_manifest_v2.csv`. It is weighted toward `needs_second_review_boundary`, which makes it most useful for stress-testing ambiguity, boundary handling, and quality/hold behavior rather than broad balanced classification performance.

Low-quality rows are quality stress cases only and are not accepted disease truth. Needs-second-review rows are uncertainty stress cases and must not be treated as accepted disease truth.

## Guardrails

- No training or fitting execution was performed.
- No model files, weights, or TFLite exports were created.
- No app/backend/runtime/model-loading files were changed.
- No model promotion is approved.
- No production claim is made.
- `reviewed_manifest_v1.csv` remains unchanged.
- `fitting_manifest_v1.csv` remains unchanged.
- `fitting_manifest_v2.csv` remains unchanged.
- Challenge rows must not be used for training.
