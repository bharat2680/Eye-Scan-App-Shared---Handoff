# reviewed_manifest_v1 Update Summary - Large DR Batch 001 Competing Buckets

## Scope

Updated the canonical `reviewed_manifest_v1.csv` for the EyeScan fundus DR
evidence lane by appending usable reviewed competing-bucket evidence from Large
DR Batch 001.

This update promotes only the usable competing-bucket rows from:

- `Google Colab/Fundus DR Hem Exudate Separation/review_batches/large_dr_batch_001_competing_buckets_proposed_addition/large_dr_batch_001_normal_or_non_specific_proposed_addition.csv`
- `Google Colab/Fundus DR Hem Exudate Separation/review_batches/large_dr_batch_001_competing_buckets_proposed_addition/large_dr_batch_001_exudate_macular_proposed_addition.csv`
- `Google Colab/Fundus DR Hem Exudate Separation/review_batches/large_dr_batch_001_competing_buckets_proposed_addition/large_dr_batch_001_mixed_hemorrhage_exudate_proposed_addition.csv`
- `Google Colab/Fundus DR Hem Exudate Separation/review_batches/large_dr_batch_001_competing_buckets_proposed_addition/large_dr_batch_001_hemorrhage_non_dr_proposed_addition.csv`

No `needs_second_review`, `unusable_low_quality`, or already-promoted
`dr_pattern_dominant` rows were included.

## Counts

- previous `reviewed_manifest_v1.csv` rows: 932
- rows appended: 2023
- new `reviewed_manifest_v1.csv` rows: 2955

Current reviewed-manifest bucket counts:

- `dr_pattern_dominant`: 932
- `normal_or_non_specific`: 472
- `exudate_macular_pattern_dominant`: 1080
- `mixed_hemorrhage_exudate_pattern`: 466
- `hemorrhage_pattern_dominant_non_dr`: 5

Current reviewed-manifest status counts:

- `accepted`: 2955

Source batch counts:

- `batch_008_kaggle_dr_224`: 98
- `large_dr_batch_001_moderate_full_review`: 2857

## Appended Row Mapping

For Large DR Batch 001 competing-bucket appended rows:

- `source_lane = fundus_dr_evidence`
- `source_batch = large_dr_batch_001_moderate_full_review`
- `source_review_batch = large_dr_batch_001_chatgpt_full_review`
- `source_dataset = Kaggle Diabetic Retinopathy Detection original 82GB train source`
- `source_class = Moderate`
- `source_row_id` uses the proposed row `batch_row_id`
- `id_code` uses `image_id`
- `image_path` uses the stable source archive member path
- `review_bucket` uses the proposed `accepted_bucket`
- `review_status = accepted`
- `reviewer = ChatGPT_visual_review`
- `review_method = conservative_contact_sheet_review`
- `accepted_at_stage = reviewed_manifest_v1_large_dr_batch_001_competing_buckets`

Source severity label `Moderate` is not used as final truth.

The `unusable_low_quality` proposal remains parked outside
`reviewed_manifest_v1.csv` for a future quality/exclusion lane.

## Verification

- appended rows: 2023
- appended `unusable_low_quality` rows: 0
- appended `needs_second_review` rows: 0
- duplicate `evidence_id`: 0
- duplicate `(source_batch, source_row_id)`: 0
- `fitting_manifest_v1.csv` remains absent.
- `challenge_manifest_v1.csv` remains absent.
- No training was performed.
- No fitting was performed.
- No model, app, backend, runtime, or preserved-package files were changed.
