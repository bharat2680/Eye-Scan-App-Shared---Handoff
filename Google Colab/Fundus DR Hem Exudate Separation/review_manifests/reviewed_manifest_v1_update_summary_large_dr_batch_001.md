# reviewed_manifest_v1 Update Summary - Large DR Batch 001

## Scope

Updated the canonical `reviewed_manifest_v1.csv` for the EyeScan fundus DR
evidence lane by appending Large DR Batch 001 accepted clean DR-pattern evidence.

This update promotes only the 834 rows from the approved proposed-addition file:

- `Google Colab/Fundus DR Hem Exudate Separation/review_batches/large_dr_batch_001_accepted_dr_pattern_proposed_addition/large_dr_batch_001_accepted_dr_pattern_proposed_addition.csv`

No downgraded, second-review, normal/non-specific, exudate, mixed,
hemorrhage-non-DR, or unusable rows were included.

## Counts

- previous `reviewed_manifest_v1.csv` rows: 98
- rows appended: 834
- new `reviewed_manifest_v1.csv` rows: 932

Current reviewed-manifest bucket/status counts:

- `review_bucket = dr_pattern_dominant`: 932
- `review_status = accepted`: 932

Source batch counts:

- `batch_008_kaggle_dr_224`: 98
- `large_dr_batch_001_moderate_full_review`: 834

## Appended Row Mapping

For Large DR Batch 001 appended rows:

- `source_lane = fundus_dr_evidence`
- `source_batch = large_dr_batch_001_moderate_full_review`
- `source_review_batch = large_dr_batch_001_chatgpt_full_review`
- `source_dataset = Kaggle Diabetic Retinopathy Detection original 82GB train source`
- `source_class = Moderate`
- `source_row_id` uses the proposed row `batch_row_id`
- `id_code` uses `image_id`
- `image_path` uses the stable source archive member path
- `review_bucket = dr_pattern_dominant`
- `review_status = accepted`
- `reviewer = ChatGPT_visual_review`
- `review_method = conservative_contact_sheet_review`
- `accepted_at_stage = reviewed_manifest_v1_large_dr_batch_001`

Source severity label `Moderate` is not used as final truth.

## Verification

- duplicate `evidence_id`: 0
- duplicate `(source_batch, source_row_id)`: 0
- `fitting_manifest_v1.csv` remains absent.
- `challenge_manifest_v1.csv` remains absent.
- No training was performed.
- No fitting was performed.
- No model, app, backend, runtime, or preserved-package files were changed.
