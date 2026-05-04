# Large DR Batch 001 Moderate Full Review

Large DR Batch 001 is a full Moderate source-label manual review pack.

## Scope

- Source: `F:\Datasets\DR-Diabetic Retinopathy\diabetic-retinopathy-detection.zip`
- Source label file: `F:\EyeScan_Local_Data\large_dr_82gb_work\labels\trainLabels.csv`
- Source selection: all `source_level = 2` rows from `trainLabels.csv`
- Source label: `Moderate`
- Selected rows: 5292
- Contact sheets: 331

## Review Rules

Source labels are severity labels only. Source labels are not accepted evidence labels.

No rows were added to `reviewed_manifest_v1.csv`. `fitting_manifest_v1.csv` and `challenge_manifest_v1.csv` remain absent. No training/fitting/model/app/backend/runtime changes were made.

Rows can only become accepted evidence after manual visual review.

Raw JPEGs were extracted only externally and were not committed.

## Allowed Future Manual Buckets

- `accept_dr_pattern_dominant`
- `downgrade_exudate_macular`
- `downgrade_mixed_hemorrhage_exudate`
- `downgrade_hemorrhage_non_dr`
- `normal_or_non_specific`
- `needs_second_review`
- `unusable_low_quality`

## Files

- `large_dr_batch_001_moderate_full_index.csv`
- `large_dr_batch_001_moderate_full_readme.md`
- `large_dr_batch_001_moderate_contact_sheets/`
