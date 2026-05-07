# Batch 008 Fitting Image Availability Audit

Date: 2026-05-07

## Scope

This is a data-availability audit only for the Batch 008 image references used by
`fitting_manifest_v1.csv`.

No training was performed.
No fitting was performed.
No model, app, backend, or runtime files were changed.
No fitting labels or split assignments were changed.
No raw images were copied into the repo by this audit.

## Source Selection

The fitting manifest was filtered to rows where `image_path` does not start with
`train/`. These rows correspond to the Batch 008 repo-relative PNG assets rather
than the Large DR archive-member JPEG paths.

## Verification Summary

- Expected Batch 008 fitting rows: `98`
- Existing on Mac: `98`
- Missing on Mac: `0`
- Fitting manifest row count: `1864`
- Reviewed manifest row count: `2955`
- `challenge_manifest_v1.csv`: absent

All 98 Batch 008 fitting rows currently resolve on this Mac as repo-relative PNG
paths under:

`Google Colab/Fundus DR Hem Exudate Separation/review_batches/batch_008_kaggle_dr_224_full_upload_pack/images/`

These 98 rows are all:

- `review_bucket = dr_pattern_dominant`
- `fitting_split = train`
- `source_batch = batch_008_kaggle_dr_224`

## Path Pattern Notes

Representative examples:

- `Google Colab/Fundus DR Hem Exudate Separation/review_batches/batch_008_kaggle_dr_224_full_upload_pack/images/moderate/row_0030_moderate_07d8db76b301.png`
- `Google Colab/Fundus DR Hem Exudate Separation/review_batches/batch_008_kaggle_dr_224_full_upload_pack/images/proliferate_dr/row_1432_proliferate_dr_d1a24527a15d.png`

These are repo-relative file paths, not `train/*.jpeg` archive members.

## Current Usability Assessment

On this Mac, the 98 Batch 008 fitting images are safe to use as-is because every
referenced file exists locally and the paths are already resolvable from the repo
checkout.

For Dell/Windows training, these 98 PNGs should not be assumed to exist just
because the fitting manifest references them. If the Dell checkout does not have
the same Batch 008 image bundle available, those files will need a deterministic
external cache or a synchronized local asset bundle before training can run
cleanly.

## Recommended Next Step

Create a Windows-side external cache or equivalent synchronized local bundle for
these same 98 Batch 008 PNG files, then add a deterministic resolver step that
maps the repo-relative Batch 008 paths to the Dell training environment in the
same way the Large DR `train/*.jpeg` rows are resolved from the external cache.

Until that is done, the future training runtime is only partially data-ready:

- Large DR fitting rows can resolve through the external cache lane
- Batch 008 fitting rows resolve on Mac
- Dell/Windows still needs a matching resolver target for the 98 Batch 008 PNGs

## Related Artifact

Per-row availability details are recorded in:

- `batch_008_fitting_image_availability_manifest.csv`
