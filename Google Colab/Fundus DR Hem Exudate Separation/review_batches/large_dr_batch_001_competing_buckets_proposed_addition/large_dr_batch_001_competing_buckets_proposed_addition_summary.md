# Large DR Batch 001 Competing Buckets Proposed Addition Summary

This folder contains proposed evidence-addition files derived from the Large DR Batch 001 ChatGPT full review findings.

This is proposed evidence-addition material only. It does not modify `reviewed_manifest_v1.csv`, does not create `fitting_manifest_v1.csv`, and does not create `challenge_manifest_v1.csv`.

## Source

- Source findings file: `Google Colab/Fundus DR Hem Exudate Separation/review_batches/large_dr_batch_001_moderate_full_review/chatgpt_full_review_findings/large_dr_batch_001_chatgpt_full_review_findings.csv`
- Source batch: `large_dr_batch_001_moderate_full_review`
- Source dataset: `Kaggle Diabetic Retinopathy Detection original 82GB train source`
- Source class/label: `Moderate`
- Source level: `2`

The source severity label `Moderate` is not used as final truth. The proposed buckets below come from conservative manual/visual review-support findings and still require final approval before any manifest promotion.

## Proposed Files And Counts

- `large_dr_batch_001_normal_or_non_specific_proposed_addition.csv`: 472 rows
- `large_dr_batch_001_exudate_macular_proposed_addition.csv`: 1080 rows
- `large_dr_batch_001_mixed_hemorrhage_exudate_proposed_addition.csv`: 466 rows
- `large_dr_batch_001_unusable_low_quality_proposed_addition.csv`: 467 rows
- `large_dr_batch_001_hemorrhage_non_dr_proposed_addition.csv`: 5 rows

Total proposed rows: 2490

## Bucket Mapping

- `normal_or_non_specific` -> `normal_or_non_specific`
- `downgrade_exudate_macular` -> `exudate_macular_pattern_dominant`
- `downgrade_mixed_hemorrhage_exudate` -> `mixed_hemorrhage_exudate_pattern`
- `downgrade_hemorrhage_non_dr` -> `hemorrhage_pattern_dominant_non_dr`
- `unusable_low_quality` -> `unusable_low_quality`

Rows with `needs_second_review` are intentionally excluded. Rows with `accept_dr_pattern_dominant` are intentionally excluded because those were already proposed and promoted through the accepted DR-pattern evidence lane.

## Verification Summary

- Normal/non-specific proposed rows: 472
- Exudate macular proposed rows: 1080
- Mixed hemorrhage/exudate proposed rows: 466
- Unusable low-quality proposed rows: 467
- Hemorrhage non-DR proposed rows: 5
- `needs_second_review` rows included: 0
- `accept_dr_pattern_dominant` rows included: 0
- Duplicate `image_id` across proposed CSVs: 0

## Safety Statement

- No training was performed.
- No fitting was performed.
- `reviewed_manifest_v1.csv` was not modified.
- `fitting_manifest_v1.csv` was not created.
- `challenge_manifest_v1.csv` was not created.
- No app/backend/runtime/model files were changed.
- No preserved package files were changed.
