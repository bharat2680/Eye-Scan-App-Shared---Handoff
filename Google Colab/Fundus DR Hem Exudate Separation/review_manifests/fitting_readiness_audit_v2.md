# Fitting Readiness Audit v2

This is a documentation-only fitting readiness audit for the EyeScan fundus DR
evidence lane after promotion of usable Large DR Batch 001 competing buckets.

Current canonical checkpoint:

- `540784d` - `data: add Large DR Batch 001 competing evidence to reviewed manifest`

Reviewed manifest:

- `Google Colab/Fundus DR Hem Exudate Separation/review_manifests/reviewed_manifest_v1.csv`

## Current Reviewed Manifest Counts

As verified after the competing-bucket promotion:

- Total rows: 2955
- `review_bucket` counts:
  - `dr_pattern_dominant`: 932
  - `exudate_macular_pattern_dominant`: 1080
  - `mixed_hemorrhage_exudate_pattern`: 466
  - `normal_or_non_specific`: 472
  - `hemorrhage_pattern_dominant_non_dr`: 5
- `review_status` counts:
  - `accepted`: 2955
- `source_batch` counts:
  - `batch_008_kaggle_dr_224`: 98
  - `large_dr_batch_001_moderate_full_review`: 2857
- `source_dataset` counts:
  - `Kaggle Diabetic Retinopathy 224x224 2019`: 98
  - `Kaggle Diabetic Retinopathy Detection original 82GB train source`: 2857

## Duplicate And Traceability Checks

The current `reviewed_manifest_v1.csv` passed the following checks:

- Duplicate `evidence_id`: 0
- Duplicate `source_batch` + `source_row_id`: 0
- Missing `image_path`: 0
- Missing `source_dataset`: 0
- Missing `review_bucket`: 0
- Missing `review_status`: 0

The manifest preserves source traceability through source batch, source dataset,
source row ID, image ID, image path/archive member, review method, source
findings file, and accepted stage.

## Fitting v1 Class Recommendation

The manifest is now ready for a fitting-manifest design proposal, but not for
immediate fitting.

For `fitting_manifest_v1`, the recommended initial class set is:

- `normal_or_non_specific`
- `dr_pattern_dominant`
- `exudate_macular_pattern_dominant`
- `mixed_hemorrhage_exudate_pattern`

These four buckets now have enough reviewed examples to support a first
structured fitting design. A proposed design should define class inclusion,
holdout strategy, source leakage controls, split policy, image access rules,
and exact exclusion criteria before any fitting CSV is created.

## Exclusion Recommendation

The following reviewed or candidate buckets should be excluded from fitting v1:

- `hemorrhage_pattern_dominant_non_dr`: only 5 reviewed examples are present,
  which is too small for a fitting class and better treated as future evidence
  to expand before inclusion.
- `unusable_low_quality`: should stay in a quality/exclusion lane rather than a
  disease-training class.
- `needs_second_review`: remains unresolved and should not enter a fitting
  manifest until manually adjudicated.

## Class Imbalance Notes

The reviewed manifest is no longer positive-only, but the proposed fitting
classes remain imbalanced:

- `exudate_macular_pattern_dominant` is largest at 1080 rows.
- `dr_pattern_dominant` has 932 rows.
- `normal_or_non_specific` has 472 rows.
- `mixed_hemorrhage_exudate_pattern` has 466 rows.

A later fitting design should use a stratified split, preserve source-level
traceability, and consider class weights or sampling controls. No training or
fitting should start until the fitting design is reviewed and approved.

## Next Safe Step

The next safe step is to create a proposed
`fitting_manifest_v1_design.md` before creating `fitting_manifest_v1.csv`.

The design should specify:

- target classes and excluded buckets
- split strategy and stratification rules
- source leakage controls
- image path/access expectations
- validation checks required before fitting
- explicit no-training boundary until the fitting manifest itself is approved

Do not create `fitting_manifest_v1.csv` yet from this audit alone.

## Safety Statement

- No training was performed.
- No fitting was performed.
- No `fitting_manifest_v1.csv` was created.
- `challenge_manifest_v1.csv` remains absent.
- `reviewed_manifest_v1.csv` was not changed by this audit.
- No app/backend/runtime/model files were changed by this audit.
- No preserved package files were changed by this audit.
- No dataset extraction or processing was performed by this audit.
