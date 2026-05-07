# Fitting V1 Image Cache Windows Result

Generated: 2026-05-07 18:24:24

## Summary

- Expected Large DR cache rows: 1766
- Cached files created/found: 1766
- Missing files: 0
- External cache root: `F:\EyeScan_Local_Data\large_dr_82gb_work\fitting_v1_image_cache`
- Source archive verified: `F:\Datasets\DR-Diabetic Retinopathy\diabetic-retinopathy-detection.zip`
- Source archive exists: yes
- Prior external source reused: `F:\EyeScan_Local_Data\large_dr_82gb_work\large_dr_batch_001_moderate_full_review\images`
- Cache creation method: NTFS hardlinks from the prior validated external Large DR Moderate extraction where possible; external copy fallback if needed.
- Cache files newly created this run: 1766
- Cache files found before creation: 0
- Hardlinks created: 1766
- External copy fallbacks: 0

## Free Space

- Free space before cache work: 399,925,628,928 bytes
- Free space after cache work: 399,924,711,424 bytes

## Temporary Archive

- Temporary `train.zip` was recreated: no
- Temporary `train.zip` was deleted: not applicable; it was not created for this run
- Temporary `train.zip` currently exists: no

## Guardrails

- Raw JPEGs were not committed to the repo.
- No training performed.
- No fitting performed.
- No model files or TFLite exports were created.
- No app/backend/runtime/model changes were made.
- `reviewed_manifest_v1.csv` was not modified.
- `fitting_manifest_v1.csv` was not modified.
- `challenge_manifest_v1.csv` remains absent.
- No full train extraction was performed.
- No test images were processed.

## Manifest Verification

- `fitting_manifest_v1.csv` rows: 1864
- Repo-relative fitting rows: 98
- Repo-relative fitting rows directly resolvable on this Dell checkout: 0
- Large DR archive-member rows: 1766
- `reviewed_manifest_v1.csv` rows: 2955
- `challenge_manifest_v1.csv` found: 0

## Windows Note

The 98 non-`train/` Batch 008 rows are repo-relative path strings in the manifest. Their raw PNG targets are not present in this Dell checkout, so they are not part of this external Large DR cache. This audit maps only the 1766 `train/*.jpeg` Large DR rows requested for the Windows external cache.
