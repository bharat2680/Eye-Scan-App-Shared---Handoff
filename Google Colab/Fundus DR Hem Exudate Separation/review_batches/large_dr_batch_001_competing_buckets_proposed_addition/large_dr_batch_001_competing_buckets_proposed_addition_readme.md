# Large DR Batch 001 Competing Buckets Proposed Addition

This folder is a proposed evidence-addition package only.

It contains candidate reviewed rows from Large DR Batch 001 that may help balance the positive-only `dr_pattern_dominant` reviewed manifest before any future fitting lane. These rows are not promoted automatically.

## Contents

- `large_dr_batch_001_normal_or_non_specific_proposed_addition.csv`
- `large_dr_batch_001_exudate_macular_proposed_addition.csv`
- `large_dr_batch_001_mixed_hemorrhage_exudate_proposed_addition.csv`
- `large_dr_batch_001_unusable_low_quality_proposed_addition.csv`
- `large_dr_batch_001_hemorrhage_non_dr_proposed_addition.csv`
- `large_dr_batch_001_competing_buckets_proposed_addition_summary.md`

## Guardrails

- This package does not modify `reviewed_manifest_v1.csv`.
- This package does not create `fitting_manifest_v1.csv`.
- This package does not create `challenge_manifest_v1.csv`.
- No training was performed.
- No fitting was performed.
- No model/app/backend/runtime changes were made.
- No preserved package changes were made.
- `needs_second_review` rows are intentionally excluded.
- Already-promoted `accept_dr_pattern_dominant` rows are intentionally excluded.

## Interpretation

The source severity label `Moderate` is not used as final truth.

The proposed accepted buckets are review-support mappings from the Large DR Batch 001 manual findings. These competing buckets should be reviewed before manifest promotion, and `unusable_low_quality` rows should be treated as a quality or exclusion pool rather than disease-training evidence.
