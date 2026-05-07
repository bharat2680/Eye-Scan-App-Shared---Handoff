# Data Path Resolution Audit

This is a data-path resolution audit for:

- `Google Colab/Fundus DR Hem Exudate Separation/review_manifests/fitting_manifest_v1.csv`

This audit does not train, fit, extract datasets, or copy raw images into the
repository.

## Summary

- Fitting manifest row count: 1864
- Unique `image_path` values: 1864
- Missing / empty `image_path` values: 0

Current path pattern mix:

- `archive_member_like`: 1766
- `repo_relative_existing`: 98

Example path patterns:

- archive-member style:
  - `train/51_left.jpeg`
  - `train/184_left.jpeg`
  - `train/195_right.jpeg`
- repo-relative extracted file style:
  - `Google Colab/Fundus DR Hem Exudate Separation/review_batches/batch_008_kaggle_dr_224_full_upload_pack/images/moderate/row_0030_moderate_07d8db76b301.png`

## Current Machine Resolvability

Direct resolution on the current Mac:

- resolvable now: 98
- unresolved now: 1766

Interpretation:

- The 98 repo-relative paths from the Batch 008 source resolve directly on the
  current machine.
- The 1766 `train/*.jpeg` paths from the Large DR 82GB source do not currently
  resolve directly on this Mac.

## External Data Requirement

The unresolved majority of rows depend on an external image staging or extract
outside the repository.

Observed local external work area:

- `/Users/bharatsharma/Documents/EyeScan_Local_Data/large_dr_82gb_work/`

Current observed contents there include:

- `reassembled/`
- `tiny_preview_extract/`
- `outer_members/`
- `train_listings/`

No matching extracted `train/*.jpeg` image tree was found there during this
audit, and sample archive-member paths such as `train/51_left.jpeg` did not
resolve to local files.

## Interpretation By Path Type

### 1. Repo-relative extracted image paths

These are already usable on the current Mac if the repository checkout remains
in place.

Count:

- 98 rows

### 2. Archive-member style paths

These act as traceability references, not directly usable file paths on the
current machine in their present form.

Count:

- 1766 rows

These rows will require one of the following in a future training runtime:

- a local extracted-image directory outside the repo plus a resolver mapping
  `train/<image>.jpeg` to real files
- a Windows/Dell external extracted-image staging location if that machine
  already has the resolved image tree
- a Mac-side extracted-image staging location created later outside the repo

## Recommended Next Step

Before any training runtime is approved, create a small resolver step that maps
archive-member paths to a stable external extracted-image root outside the repo.

Practical next step:

- decide whether the canonical baseline runtime will use:
  - Mac external extracted images, or
  - Windows/Dell external extracted images
- then update the training notebook or a future runtime helper to resolve
  `train/*.jpeg` references deterministically
- keep raw images outside the repo

## Safety Statement

- No training was performed.
- No fitting was performed.
- No dataset extraction was performed.
- No raw images were copied into the repository.
- `fitting_manifest_v1.csv` was not modified.
- `reviewed_manifest_v1.csv` was not modified.
- `challenge_manifest_v1.csv` remains absent.
- No app/backend/runtime/model files were changed.
