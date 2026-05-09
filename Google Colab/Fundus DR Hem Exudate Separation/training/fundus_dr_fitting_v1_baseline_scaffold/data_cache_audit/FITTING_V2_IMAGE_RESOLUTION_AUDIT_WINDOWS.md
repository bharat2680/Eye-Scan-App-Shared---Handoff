# Fitting Manifest v2 Image Resolution Audit: Windows

## Scope

This audit verifies Dell/Windows image path resolution for canonical `fitting_manifest_v2.csv`. It does not copy raw images into the repo, run training, execute fitting, export models, export TFLite, modify app/backend/runtime/model-loading files, or promote any model.

## Inputs

- Manifest: `Google Colab/Fundus DR Hem Exudate Separation/review_manifests/fitting_manifest_v2.csv`
- Large DR cache root: `F:\EyeScan_Local_Data\large_dr_82gb_work\fitting_v1_image_cache\`
- Batch 008 cache root: `F:\EyeScan_Local_Data\large_dr_82gb_work\fitting_v1_batch_008_image_cache\`
- Batch 008 mapping: `batch_008_fitting_image_cache_manifest_windows.csv`

## Outputs

- Repo audit CSV: `fitting_v2_image_resolution_audit_windows.csv`
- External resolved manifest: `F:\EyeScan_Local_Data\large_dr_82gb_work\fitting_v2_resolved_manifest_windows.csv`

## Resolution Rules

- `image_path` values starting with `train/` resolve under the Large DR cache root.
- Batch 008 PNG rows resolve using the existing Batch 008 Windows cache manifest and external cache root.

## Count Verification

- Total rows: 1696
- Resolved rows: 1696
- Missing rows: 0
- Large DR rows: 1603
- Batch 008 rows: 93

## Class Counts

- `normal_or_non_specific`: 424
- `dr_pattern_dominant`: 424
- `exudate_macular_pattern_dominant`: 424
- `mixed_hemorrhage_exudate_pattern`: 424

## Split Counts

- `train`: 1184
- `val`: 256
- `test`: 256

## Guardrails

- `fitting_manifest_v2.csv` was not modified.
- `fitting_manifest_v1.csv` was not modified.
- `reviewed_manifest_v1.csv` was not modified.
- `challenge_manifest_v1.csv` remains absent.
- No raw images were copied into the repo.
- No training/model/app/backend/runtime changes were made.

## Git Diff Summary

Expected repo diff for this task: this markdown audit and `fitting_v2_image_resolution_audit_windows.csv` only.