# fitting_manifest_v1 Design

This is a design document only. It does not create `fitting_manifest_v1.csv`.

Current canonical checkpoint:

- `51e3694` - `docs: audit fitting readiness after competing bucket promotion`

Canonical reviewed source:

- `Google Colab/Fundus DR Hem Exudate Separation/review_manifests/reviewed_manifest_v1.csv`

## Purpose

`fitting_manifest_v1.csv` should be a curated training-preparation manifest
derived from `reviewed_manifest_v1.csv`.

The fitting manifest should select reviewed, accepted rows; define included
classes; preserve evidence/source traceability; and assign train/validation/test
splits only after the fitting design is approved.

This task creates the design only. `fitting_manifest_v1.csv` is not created.

## Included Classes For Fitting v1

The recommended first fitting manifest should include four classes:

- `normal_or_non_specific`
- `dr_pattern_dominant`
- `exudate_macular_pattern_dominant`
- `mixed_hemorrhage_exudate_pattern`

These are the reviewed buckets with enough accepted evidence for an initial
controlled fitting design.

## Excluded Buckets

The following buckets should be excluded from fitting v1:

- `hemorrhage_pattern_dominant_non_dr`: count is only 5, which is too small for
  a fitting class.
- `unusable_low_quality`: belongs to quality/exclusion handling, not disease
  fitting.
- `needs_second_review`: unresolved and not eligible for fitting.
- Any non-accepted rows.

## Current Available Counts

Current reviewed, accepted rows available for the recommended four-class fitting
design:

- `normal_or_non_specific`: 472
- `dr_pattern_dominant`: 932
- `exudate_macular_pattern_dominant`: 1080
- `mixed_hemorrhage_exudate_pattern`: 466

Total usable four-class rows available: 2950

Excluded reviewed bucket:

- `hemorrhage_pattern_dominant_non_dr`: 5

## Proposed Fitting Strategy

### Option A - Balanced Cap

Use a balanced cap of 466 rows per included class.

- `normal_or_non_specific`: 466 of 472
- `dr_pattern_dominant`: 466 of 932
- `exudate_macular_pattern_dominant`: 466 of 1080
- `mixed_hemorrhage_exudate_pattern`: 466 of 466

Expected fitting rows: 1864

This leaves larger classes partially unused for future challenge, holdout, or
later fitting expansion.

### Option B - Near-Full With Class Weights

Use all 2950 usable rows from the four included classes.

This would require a stratified split and likely class weights or sampling
controls later:

- `normal_or_non_specific`: 472
- `dr_pattern_dominant`: 932
- `exudate_macular_pattern_dominant`: 1080
- `mixed_hemorrhage_exudate_pattern`: 466

This is not preferred for the first baseline unless explicitly chosen later.

### Recommendation

Prefer Option A for the first fitting baseline.

Option A is simpler, balanced, easier to audit, and safer for a first controlled
baseline. It also preserves surplus rows from larger classes for later holdout,
challenge, or fitting expansion decisions.

## Split Strategy Proposal

If Option A is chosen later:

- Use a stratified split by `review_bucket`.
- Suggested split:
  - train: 70%
  - validation: 15%
  - internal test: 15%
- Preserve `source_batch`, `source_dataset`, `evidence_id`, and `source_row_id`
  traceability in all split rows.
- No patient-level grouping is currently available unless `image_id` metadata
  can reliably support it. This limitation should be documented in the dry-run
  manifest.

Approximate Option A split shape per class:

- 326 train rows
- 70 validation rows
- 70 internal test rows

Exact split counts should be generated deterministically in a later dry-run
step.

## Leakage Controls

A future fitting dry-run should enforce:

- no duplicate `image_id` across splits
- no duplicate `evidence_id`
- no duplicate `source_batch` + `source_row_id`
- preserve `source_batch` and `source_dataset` columns
- preserve `evidence_id`, `source_row_id`, `id_code`, and `image_path`
- do not mix accepted and unresolved rows
- do not include `needs_second_review`
- do not include `unusable_low_quality` in disease fitting
- do not include non-accepted rows

## Future Challenge Manifest

`challenge_manifest_v1.csv` should be created separately later.

A future challenge manifest should focus on hard examples, mixed or uncertain
cases, source-shift checks, and possibly excluded quality cases. It should not
be created as part of this design task.

This task does not create `challenge_manifest_v1.csv`.

## No-Training Safety Statement

- No fitting manifest was created.
- No challenge manifest was created.
- No training was performed.
- No fitting was performed.
- `reviewed_manifest_v1.csv` was not modified.
- No model/app/backend/runtime files were changed.
- No preserved package files were changed.
- No dataset extraction or processing was performed.

## Recommended Next Step

After this design is accepted, create a proposed
`fitting_manifest_v1_dry_run.csv`.

The dry-run should implement the approved option, most likely Option A with
1864 rows, and should include deterministic split assignment plus verification
summaries. Do not train until the dry-run is reviewed and a canonical
`fitting_manifest_v1.csv` is explicitly approved.
