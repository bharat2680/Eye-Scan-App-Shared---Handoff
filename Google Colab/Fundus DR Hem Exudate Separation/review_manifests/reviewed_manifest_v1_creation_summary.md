# reviewed_manifest_v1 Creation Summary

## Scope

Created the first canonical `reviewed_manifest_v1.csv` for the EyeScan fundus DR
evidence lane.

This manifest starts with Batch 008 accepted DR-pattern evidence only.

Historical Batches 001-007 are not backfilled in this step and can be added
later through a separate reviewed-manifest backfill task.

## Source

Rows were copied from the approved dry-run file:

- `Google Colab/Fundus DR Hem Exudate Separation/review_manifests/proposed_reviewed_manifest_v1_schema/reviewed_manifest_v1_dry_run_batch_008_only.csv`

The dry-run was derived from the proposed Batch 008 accepted DR-pattern addition:

- Batch 008A accepted rows: 14
- Batch 008B accepted rows: 84
- total rows: 98

## Verification

- `reviewed_manifest_v1.csv` row count: 98
- unique `evidence_id` values: 98
- duplicate `evidence_id` values: 0
- unique `source_row_id` values: 98
- duplicate `source_row_id` values: 0
- `review_bucket = dr_pattern_dominant`: 98
- `review_status = accepted`: 98
- `source_batch = batch_008_kaggle_dr_224`: 98

## Safety Boundary

- No `fitting_manifest_v1.csv` was created.
- No `challenge_manifest_v1.csv` was created.
- No training was performed.
- No fitting was performed.
- No model changes were made.
- No app, backend, runtime, or model-loading changes were made.
- No preserved package changes were made.
- The 82GB diabetic-retinopathy-detection dataset was not inspected or processed.
