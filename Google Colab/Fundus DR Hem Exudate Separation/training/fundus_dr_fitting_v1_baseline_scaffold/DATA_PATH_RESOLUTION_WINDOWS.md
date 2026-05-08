# Windows Data Path Resolution

This note is specific to Dell/Windows fitting-manifest resolution for:

- `Google Colab/Fundus DR Hem Exudate Separation/review_manifests/fitting_manifest_v1.csv`

It documents how the current Dell workstation resolves every fitting row to an
external cached image path without copying raw images into the repository.

## External Cache Roots

- Large DR cache root:
  `F:\EyeScan_Local_Data\large_dr_82gb_work\fitting_v1_image_cache\`
- Batch 008 cache root:
  `F:\EyeScan_Local_Data\large_dr_82gb_work\fitting_v1_batch_008_image_cache\`

## Mapping Rules

- Rows where `image_path` starts with `train/` resolve under the Large DR cache.
- Large DR resolution is backed by:
  `data_cache_audit/fitting_v1_image_cache_manifest_windows.csv`
- Rows where `image_path` does not start with `train/` are the Batch 008 PNG
  rows and resolve through the Batch 008 external cache audit mapping.
- Batch 008 resolution is backed by:
  `data_cache_audit/batch_008_fitting_image_cache_manifest_windows.csv`

## Expected Resolution Counts On Dell

- Total expected resolvable rows: `1864`
- Large DR expected: `1766`
- Batch 008 expected: `98`

The current Dell cache audit establishes `1864 / 1864` resolvable fitting rows
without requiring any raw image files in the repository.

## Repo Safety

- Raw images are not committed to the repository.
- This scaffold resolves image paths for validation only.
- No training, fitting, model export, or TFLite generation is part of this
  Windows resolver.

## Environment Scope

This mapping is Dell/Windows-specific.

- Mac or Colab may need separate cache roots.
- Mac or Colab may require different mounted-drive mappings.
- Any future runtime should treat these Windows cache roots as local environment
  configuration, not portable repo paths.

## Local Resolver

Use:

- `scripts/resolve_fitting_manifest_images_windows.py`

By default, that script writes a generated local-only resolved manifest outside
the repo to:

- `F:\EyeScan_Local_Data\large_dr_82gb_work\fitting_v1_resolved_manifest_windows.csv`
