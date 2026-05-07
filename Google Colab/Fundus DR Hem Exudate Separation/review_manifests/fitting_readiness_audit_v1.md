# Fitting Readiness Audit v1

This is a documentation-only readiness audit for the EyeScan fundus DR evidence lane after the Large DR Batch 001 accepted-evidence update.

Current canonical checkpoint:

- `6e2e358` - `data: add Large DR Batch 001 accepted evidence to reviewed manifest`

Reviewed manifest:

- `Google Colab/Fundus DR Hem Exudate Separation/review_manifests/reviewed_manifest_v1.csv`

## Current Reviewed Manifest Counts

As verified after the Large DR Batch 001 update:

- Total rows: 932
- `review_bucket` counts:
  - `dr_pattern_dominant`: 932
- `review_status` counts:
  - `accepted`: 932
- `source_batch` counts:
  - `batch_008_kaggle_dr_224`: 98
  - `large_dr_batch_001_moderate_full_review`: 834
- `source_dataset` counts:
  - `Kaggle Diabetic Retinopathy 224x224 2019`: 98
  - `Kaggle Diabetic Retinopathy Detection original 82GB train source`: 834

## Duplicate And Traceability Checks

The current `reviewed_manifest_v1.csv` passed the following checks:

- Duplicate `evidence_id`: 0
- Duplicate `source_batch` + `source_row_id`: 0
- Missing `image_path`: 0
- Missing `source_dataset`: 0
- Missing `review_bucket`: 0
- Missing `review_status`: 0

The manifest preserves source traceability through source batch, source dataset, source row ID, image ID, and image path/archive-member fields.

## Readiness Assessment

The reviewed manifest is not suitable for fitting yet.

Reason: the current canonical reviewed manifest contains only positive `dr_pattern_dominant` accepted evidence. It does not yet include reviewed negative examples, competing abnormality buckets, or quality gate examples needed to make a fitting manifest balanced and interpretable.

Before fitting, the lane should add reviewed evidence for at least the following buckets:

- `normal_or_non_specific`
- `exudate_macular_pattern_dominant`
- `mixed_hemorrhage_exudate_pattern`
- `hemorrhage_pattern_dominant_non_dr`
- `unusable_low_quality` / quality gate examples

Rows marked `needs_second_review` should remain excluded from any fitting manifest until they receive a later manual decision.

## Recommended Next Evidence Lanes

Do not create `fitting_manifest_v1.csv` yet while the canonical reviewed manifest contains only positive DR-pattern rows.

The next likely lane should add reviewed negatives and competing abnormal buckets before fitting. Candidate sources already available from prior review work include:

- Large DR Batch 001 downgraded, normal/non-specific, unusable, and second-review rows.
- Batch 008A and Batch 008B downgraded rows.
- Batches 001-007 historical reviewed evidence, if it can be backfilled into the canonical reviewed-manifest schema with source traceability preserved.

Any future fitting lane should be created only after reviewed class coverage includes both accepted positive evidence and reviewed competing/negative evidence.

## Safety Statement

- No training was performed.
- No fitting was performed.
- No `fitting_manifest_v1.csv` was created.
- `challenge_manifest_v1.csv` remains absent.
- `reviewed_manifest_v1.csv` was not changed by this audit.
- No app/backend/runtime/model files were changed by this audit.
- No preserved package files were changed by this audit.
- No dataset extraction or processing was performed by this audit.
