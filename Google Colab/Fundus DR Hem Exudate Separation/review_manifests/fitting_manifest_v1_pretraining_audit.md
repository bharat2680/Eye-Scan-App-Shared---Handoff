# fitting_manifest_v1 Pretraining Audit

This is a documentation-only pretraining audit for the EyeScan fundus DR
evidence lane after creation of the canonical `fitting_manifest_v1.csv`.

Current canonical checkpoint:

- `9b30470` - `data: create fitting manifest v1 from approved dry-run`

Audited files:

- `Google Colab/Fundus DR Hem Exudate Separation/review_manifests/fitting_manifest_v1.csv`
- `Google Colab/Fundus DR Hem Exudate Separation/review_manifests/reviewed_manifest_v1.csv`

## fitting_manifest_v1 Counts

Verified `fitting_manifest_v1.csv` counts:

- Total rows: 1864

Class counts:

- `normal_or_non_specific`: 466
- `dr_pattern_dominant`: 466
- `exudate_macular_pattern_dominant`: 466
- `mixed_hemorrhage_exudate_pattern`: 466

Split counts:

- `train`: 1304
- `val`: 280
- `test`: 280

Class-by-split counts:

- `normal_or_non_specific`
  - `train`: 326
  - `val`: 70
  - `test`: 70
- `dr_pattern_dominant`
  - `train`: 326
  - `val`: 70
  - `test`: 70
- `exudate_macular_pattern_dominant`
  - `train`: 326
  - `val`: 70
  - `test`: 70
- `mixed_hemorrhage_exudate_pattern`
  - `train`: 326
  - `val`: 70
  - `test`: 70

## Data Integrity Checks

The following integrity checks passed:

- `evidence_id` unique: yes
- duplicate `evidence_id`: 0
- duplicate `image_path`: 0
- duplicate `source_batch` + `source_row_id`: 0
- all fitting-manifest `evidence_id` values exist in `reviewed_manifest_v1.csv`
- fitting classes match reviewed `review_bucket` values
- `review_status = accepted` for all fitting rows

Excluded buckets were not included:

- `hemorrhage_pattern_dominant_non_dr`: 0 rows
- `unusable_low_quality`: 0 rows
- unresolved / `needs_second_review`: 0 rows

## Traceability

Source batch counts:

- `large_dr_batch_001_moderate_full_review`: 1766
- `batch_008_kaggle_dr_224`: 98

Source dataset counts:

- `Kaggle Diabetic Retinopathy Detection original 82GB train source`: 1766
- `Kaggle Diabetic Retinopathy 224x224 2019`: 98

Image path / archive-member availability:

- missing `image_path`: 0
- all rows retain `image_path` values for source traceability

The fitting manifest stores referenced image paths or archive-member style paths
for traceability. Raw images are not committed as part of this fitting-manifest
creation step.

## Training-Readiness Recommendation

`fitting_manifest_v1.csv` is ready for a small baseline training experiment.

That baseline should be treated as an evaluation-oriented first run only, not a
production model lane. Recommended outputs for the first experiment are:

- training/validation/test metrics
- confusion matrix
- class-level error review notes

Do not use the first baseline as approval for app/backend integration. Any
integration lane should wait for baseline results, error analysis, and a later
explicit decision.

## Safety Statement

- No training was performed.
- No fitting execution was performed.
- No model files were changed.
- No backend, app, or runtime files were changed.
- `reviewed_manifest_v1.csv` remains unchanged at 2955 rows.
- `fitting_manifest_v1.csv` remains unchanged by this audit.
- `challenge_manifest_v1.csv` remains absent.
- No preserved package files were changed.
