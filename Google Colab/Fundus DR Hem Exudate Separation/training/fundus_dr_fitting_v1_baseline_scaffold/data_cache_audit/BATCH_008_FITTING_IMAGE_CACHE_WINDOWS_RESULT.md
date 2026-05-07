# Batch 008 Fitting Image Cache Windows Result

Generated: 2026-05-07 18:54:48

## Summary

- Expected Batch 008 cache rows: 98
- Found in Dell checkout: 0
- Cached externally: 0
- Missing: 98
- External cache root: `F:\EyeScan_Local_Data\large_dr_82gb_work\fitting_v1_batch_008_image_cache`
- External cache PNG count now: 0
- External cache PNG bytes now: 0
- Free space before audit/cache work: 399,924,711,424 bytes
- Free space after audit/cache work: 399,924,711,424 bytes

## Source Interpretation

Batch 008 rows were identified from `fitting_manifest_v1.csv` where `image_path` does not start with `train/`.

- Fitting manifest rows: 1864
- Large DR `train/` rows: 1766
- Batch 008 non-`train/` rows: 98
- Reviewed manifest rows: 2955
- `challenge_manifest_v1.csv` found: 0

The canonical Mac-side availability audit at `BATCH_008_FITTING_IMAGE_AVAILABILITY_AUDIT.md` reports these 98 PNGs as available on Mac. This Dell/Windows audit checks only whether the same repo-relative source paths exist in this Dell checkout.

## Dell/Windows Availability

- Safe to use from Dell checkout as-is: no
- Needs external training cache or synchronized asset bundle for Dell/Windows: yes

No PNG source files were found in the Dell checkout for the 98 Batch 008 fitting rows, so no raw PNGs were copied or fabricated.

## Recommended Next Step

Copy the Batch 008 upload-pack image files from the Mac-side checkout/artifact source into a Dell-accessible external cache, then rerun this audit to populate/verify the 98 PNG mappings.

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
