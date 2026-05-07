# fitting_manifest_v1 Creation Summary

## Scope

Created the first canonical `fitting_manifest_v1.csv` for the EyeScan fundus DR
evidence lane from the approved dry-run fitting manifest.

This step copies the approved dry-run rows and preserves their schema, class
selection, and split assignments exactly.

## Source

Rows were copied from:

- `Google Colab/Fundus DR Hem Exudate Separation/review_manifests/proposed_fitting_manifest_v1/fitting_manifest_v1_dry_run.csv`

The canonical output is:

- `Google Colab/Fundus DR Hem Exudate Separation/review_manifests/fitting_manifest_v1.csv`

## Counts

- `fitting_manifest_v1.csv` row count: 1864

Class counts:

- `normal_or_non_specific`: 466
- `dr_pattern_dominant`: 466
- `exudate_macular_pattern_dominant`: 466
- `mixed_hemorrhage_exudate_pattern`: 466

Split counts:

- `train`: 1304
- `val`: 280
- `test`: 280

## Verification

- `evidence_id` unique: yes
- duplicate `evidence_id`: 0
- duplicate `image_path`: 0
- `reviewed_manifest_v1.csv` remains unchanged at 2955 rows.
- `challenge_manifest_v1.csv` remains absent.

## Safety Statement

- `fitting_manifest_v1.csv` was created from the approved dry-run only.
- No training was performed.
- No fitting was performed.
- `challenge_manifest_v1.csv` was not created.
- `reviewed_manifest_v1.csv` was not modified.
- Fitting v1 uses four balanced classes at 466 rows each.
- No model, app, backend, runtime, or preserved-package files were changed.
