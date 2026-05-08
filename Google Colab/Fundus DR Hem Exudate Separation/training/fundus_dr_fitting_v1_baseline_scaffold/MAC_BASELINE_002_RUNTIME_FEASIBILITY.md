# Mac Baseline 002 Runtime Feasibility Audit

Generated: 2026-05-08

## Scope

This is a runtime and storage feasibility audit only for a possible Mac Baseline
002 run using the existing `fitting_manifest_v1.csv`.

No training was performed.
No fitting was performed.
No packages were installed.
No files were deleted.
No cleanup was performed.
No model files or TFLite exports were created.
No app, backend, runtime, or model files were changed.
`reviewed_manifest_v1.csv` and `fitting_manifest_v1.csv` were not modified.
`challenge_manifest_v1.csv` remains absent.
No raw images were copied into the repo.

## Current Storage State

Macintosh HD data volume:

- Size: `228 GiB`
- Used: `192 GiB`
- Available: `15 GiB`
- Available bytes: `15,837,745,152`
- Available GiB: `14.75`
- Capacity used: `93%`

This is below the recommended headroom for a local PyTorch/MPS baseline run.

## Minimum Safe Free Space Estimate

Before Baseline 002 on Mac, recommended local free space is at least `30-50 GiB`.

Reasoning:

- PyTorch and torchvision environment: roughly several GiB after wheels,
  dependencies, and package caches
- Torch/model cache and downloaded pretrained weights: roughly 1-3 GiB depending
  architecture and cache reuse
- Run outputs, logs, metrics, plots, and any temporary tensors/checkpoints:
  several GiB if checkpoints are enabled
- macOS swap and memory pressure headroom: 15-25 GiB is a safer floor for a
  training run, especially if MPS/CPU memory behavior is not yet characterized

The current `14.75 GiB` free is too tight for a comfortable local baseline.

## External Drive Checks

Mounted external volumes:

- `/Volumes/My Passport`
- `/Volumes/WD Unlocker`

My Passport cache status from the prior resolver audit:

- Large DR cache readable: yes
- Batch 008 cache readable: yes
- Total fitting rows resolved from external caches: `1864 / 1864`

Writeability checks:

- `/Volumes/My Passport`: not writable
- `/Volumes/My Passport/EyeScan_Local_Data`: not writable
- `/Volumes/My Passport/EyeScan_Local_Data/large_dr_82gb_work`: not writable
- Large DR cache root: not writable
- Batch 008 cache root: not writable
- `/Volumes/WD Unlocker`: read-only

Mount details show My Passport mounted as `ntfs` with `read-only`.

Conclusion: My Passport is suitable as a read-only image source for Mac, but it
is not currently suitable as an output/checkpoint target on this Mac.

## Local Runtime Check

Default Mac Python:

- Python version: `3.10.13`
- Python executable: `/Users/bharatsharma/.pyenv/versions/3.10.13/bin/python3`
- `torch`: not installed
- `torchvision`: not installed
- MPS available: no, because `torch` is not installed
- CPU fallback hardware path: available, but PyTorch still needs to be installed
  or an approved environment selected

No packages were installed during this audit.

## Cleanup Candidates

These are inventory candidates only. Nothing was deleted.

| Risk level | Path | Approx size | Notes |
|---|---:|---:|---|
| `review_before_delete` | `/Users/bharatsharma/Library/Developer/Xcode/iOS DeviceSupport/iPhone15,3 26.3.1 (23D771330a)` | `5.4 GiB` | Old device-support symbols can often be removed if not needed for that device/iOS version, but verify first. |
| `review_before_delete` | `/Users/bharatsharma/Library/Developer/CoreSimulator` | `1.1 GiB` | Simulator data; review active simulator needs before cleanup. |
| `review_before_delete` | `/Users/bharatsharma/Documents/EyeScan_Local_Data` | `1.0 GiB` | Internal local EyeScan data; inspect before deletion. |
| `review_before_delete` | `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/Google Colab/Fundus DR Hem Exudate Separation/review_batches/contact_sheets` | `534 MiB` | Review-support contact sheets; may still be useful for evidence traceability. |
| `review_before_delete` | `/Users/bharatsharma/Downloads` | `414 MiB` | General user downloads; inspect manually. |
| `safe_candidate` | `/Users/bharatsharma/Library/Caches/pip` | `596 KiB` | Tiny; cleanup would not materially help. |
| `safe_candidate` | `/Users/bharatsharma/Documents/Playground/_backend_patch_staging/.pytest_cache` | `20 KiB` | Tiny Python test cache. |
| `review_before_delete` | `/Users/bharatsharma/.pub-cache` | `302 MiB` | Flutter/Dart package cache; can be regenerated but may slow future builds. |
| `review_before_delete` | `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/Google Colab/Fundus DR Hem Exudate Separation/review_batches/batch_008_kaggle_dr_224_full_upload_pack` | `140 MiB` | Batch 008 raw/review support assets; do not delete unless the lane no longer needs local visual traceability. |
| `review_before_delete` | `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/Google Colab/Fundus DR Hem Exudate Separation/review_batches/batch_008_kaggle_dr_224_full_review_pack` | `28 MiB` | Review-support pack; small. |
| `review_before_delete` | `/Users/bharatsharma/Desktop/Eye_Scan App Timeline/Fundus_Broad_Abnormality_V1_EfficientNetB0-20260430T114328Z-3-001.zip` | `133 MiB` | Archive-like artifact; inspect before deleting. |
| `review_before_delete` | `/Users/bharatsharma/Desktop/batch_008_fitting_98_transfer_for_dell` | `6.9 MiB` | Transfer package folder; keep until Dell transfer is fully verified. |
| `review_before_delete` | `/Users/bharatsharma/Desktop/batch_008_fitting_98_transfer_for_dell.zip` | `6.6 MiB` | Transfer ZIP; keep until Dell transfer is fully verified. |
| `do_not_touch` | `/Volumes/My Passport/EyeScan_Local_Data/large_dr_82gb_work/fitting_v1_image_cache` | external | Required external Large DR fitting cache. |
| `do_not_touch` | `/Volumes/My Passport/EyeScan_Local_Data/large_dr_82gb_work/fitting_v1_batch_008_image_cache` | external | Required external Batch 008 fitting cache. |
| `do_not_touch` | `reviewed_manifest_v1.csv` | repo data | Canonical reviewed evidence manifest. |
| `do_not_touch` | `fitting_manifest_v1.csv` | repo data | Canonical fitting manifest. |

Large file scan under `/Users/bharatsharma/Documents/Playground` did not find
obvious single derived artifacts over `200 MiB` outside the listed review-support
areas.

## Runtime Options

### A. Continue Baseline 002 On Dell

Recommended immediate path.

Dell has already run Baseline 001 and has the Windows external cache lane
configured. This avoids Mac storage pressure and avoids setting up a new PyTorch
environment on a nearly full internal disk.

### B. Run Baseline 002 On Mac After Freeing 30-50 GiB

Possible later.

Mac data resolution is ready, but local storage and Python dependencies are not.
Before using Mac, free at least `30-50 GiB`, then set up an approved PyTorch
environment and re-run the resolver check inside that environment.

### C. Use Colab Or Kaggle GPU

Potentially attractive for speed, but it needs a portable data bundle or remote
resolver first. The current Mac/Dell cache layout is external-drive based, not a
cloud-ready dataset package.

### D. Use Mac With External Writable Output Drive

Not currently feasible with My Passport as mounted, because it is read-only on
Mac. This becomes viable only if a writable external output path is available or
My Passport is remounted/reformatted/configured with safe write support.

## Recommendation

Choose option A for the next Baseline 002 attempt: continue on Dell because it is
already configured and avoids Mac storage/runtime setup risk.

Mac should remain a data-verification and audit machine for this lane until one
of these changes is made:

- internal free space is increased to at least `30-50 GiB`, and an approved
  PyTorch/torchvision environment is installed
- or a writable external output/checkpoint drive is made available
- or a cloud GPU data bundle/resolver is prepared

This audit does not approve model promotion, app/backend integration, or any
training run by itself.

## Final Guardrail Verification

- `fitting_manifest_v1.csv` remains `1864` rows
- `reviewed_manifest_v1.csv` remains `2955` rows
- `challenge_manifest_v1.csv` remains absent
- no training was run
- no packages were installed
- no cleanup was performed
- no raw images were copied into the repo
