# Fitting V1 Mac Resolver Feasibility

Generated: 2026-05-08

## Scope

This is a Mac resolver and runtime feasibility audit for a future Baseline 002
run using the existing `fitting_manifest_v1.csv`.

No training was performed.
No fitting was performed.
No model files or TFLite exports were created.
No app, backend, runtime, or model files were changed.
`reviewed_manifest_v1.csv` and `fitting_manifest_v1.csv` were not modified.
`challenge_manifest_v1.csv` remains absent.
No raw images were copied into the repo.

## External Cache Roots Checked

Large DR cache:

`/Volumes/My Passport/EyeScan_Local_Data/large_dr_82gb_work/fitting_v1_image_cache/`

Batch 008 cache:

`/Volumes/My Passport/EyeScan_Local_Data/large_dr_82gb_work/fitting_v1_batch_008_image_cache/`

## Mount And Cache Availability

- `/Volumes/My Passport`: mounted
- Large DR cache root exists: yes
- Batch 008 cache root exists: yes
- Batch 008 cache images folder exists: yes
- Mac read probe from Large DR cache: passed
- Mac read probe from Batch 008 cache: passed

Observed cache file counts:

- Large DR external JPEGs: `1766`
- Batch 008 external PNGs: `98`

## Fitting Manifest Resolver Result

The resolver mapped all `fitting_manifest_v1.csv` rows as follows:

- `train/*.jpeg` rows -> Large DR cache
- non-`train/` Batch 008 PNG rows -> Batch 008 cache using the external transfer manifest

Counts:

- Fitting manifest rows: `1864`
- Large DR rows expected: `1766`
- Large DR rows resolved: `1766`
- Batch 008 rows expected: `98`
- Batch 008 rows resolved: `98`
- Total resolved: `1864`
- Missing: `0`

Class counts:

- `normal_or_non_specific`: `466`
- `dr_pattern_dominant`: `466`
- `exudate_macular_pattern_dominant`: `466`
- `mixed_hemorrhage_exudate_pattern`: `466`

Split counts:

- `train`: `1304`
- `val`: `280`
- `test`: `280`

Per-row Mac cache mapping is recorded in:

- `fitting_v1_image_cache_manifest_mac.csv`

## Runtime Check

Default Mac Python checked:

- Python version: `3.10.13`
- Python executable: `/Users/bharatsharma/.pyenv/versions/3.10.13/bin/python3`
- Platform: `macOS-26.4.1-arm64-arm-64bit`
- `torch` installed: no
- `torchvision` installed: no
- MPS available: no, because `torch` is not installed in this Python environment
- CPU fallback hardware/runtime path: available, but PyTorch CPU execution still requires `torch`

No packages were installed during this audit.

## Feasibility Assessment

The Mac data resolver is ready for Baseline 002: all `1864` fitting rows resolve
from the external My Passport caches with zero missing files.

The default Mac Python runtime is not ready to execute Baseline 002 yet because
`torch` and `torchvision` are not installed. Baseline 002 should not be started
until an approved Python environment is selected or dependencies are explicitly
approved for installation.

## Recommended Next Step

Before any Baseline 002 run:

1. Choose or create an approved Mac training environment with `torch` and
   `torchvision`.
2. Re-run this resolver audit or the Mac resolver check inside that environment.
3. Start Baseline 002 only after confirming the same `1864 / 1864` image
   resolution and an available compute backend.

This audit does not approve app/backend integration or model promotion.
