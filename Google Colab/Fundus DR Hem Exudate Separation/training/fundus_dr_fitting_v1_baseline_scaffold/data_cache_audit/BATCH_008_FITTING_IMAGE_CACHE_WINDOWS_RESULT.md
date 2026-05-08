# Batch 008 Fitting Image Cache Windows Result

Generated: 2026-05-08 11:37:39

## Summary

- Expected Batch 008 cache rows: 98
- Found/cached externally: 98
- Missing: 0
- External cache root: `F:\EyeScan_Local_Data\large_dr_82gb_work\fitting_v1_batch_008_image_cache`
- Transfer manifest used: `F:\EyeScan_Local_Data\large_dr_82gb_work\fitting_v1_batch_008_image_cache\batch_008_fitting_98_transfer_manifest.csv`
- External cache PNG count now: 98
- External cache PNG bytes now: 6934155
- Large DR external cached JPEG count: 1766
- Total fitting images externally/resolvably available on Dell: 1864
- Current F: free space after audit update: 399,910,522,880 bytes

## Source Interpretation

Batch 008 rows were identified from `fitting_manifest_v1.csv` where `image_path` does not start with `train/`. The Large DR rows continue to resolve through the separate Windows external JPEG cache.

- Fitting manifest rows: 1864
- Large DR `train/` rows: 1766
- Batch 008 non-`train/` rows: 98
- Reviewed manifest rows: 2955
- `challenge_manifest_v1.csv` found: 0

## Dell/Windows Availability

The Mac-created Batch 008 transfer bundle is now present under the Dell external cache root and has been extracted there. Its transfer manifest maps each Batch 008 `evidence_id` and original repo-relative `image_path` to a copied PNG filename under `images/`.

- Safe to use from Dell checkout as-is: no, these repo-relative PNGs are still not committed in this checkout.
- Safe to use from Dell external cache: yes, all 98 Batch 008 fitting PNGs are present externally.
- Raw PNGs committed to repo: 0

## Recommended Next Step

For a future training dry-run, configure the Windows data resolver to read Large DR `train/*.jpeg` rows from `F:\EyeScan_Local_Data\large_dr_82gb_work\fitting_v1_image_cache` and Batch 008 PNG rows from `F:\EyeScan_Local_Data\large_dr_82gb_work\fitting_v1_batch_008_image_cache\images` using the per-row mapping in this audit.

## Guardrails

- Raw PNGs were not committed to the repo.
- No training was performed.
- No fitting was performed.
- No model files or TFLite exports were created.
- No app/backend/runtime/model changes were made.
- `reviewed_manifest_v1.csv` was not modified.
- `fitting_manifest_v1.csv` was not modified.
- `challenge_manifest_v1.csv` remains absent.
- Fitting labels and splits were not changed.

## Per-Row Mapping

Per-row Windows cache availability is recorded in:

- `batch_008_fitting_image_cache_manifest_windows.csv`
