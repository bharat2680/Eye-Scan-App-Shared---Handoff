# fitting_manifest_v1 Dry-Run Summary

This is a dry-run fitting manifest only. It does not create the canonical
`fitting_manifest_v1.csv`, does not create `challenge_manifest_v1.csv`, and
does not perform any training or fitting.

## Source

- Source manifest:
  `Google Colab/Fundus DR Hem Exudate Separation/review_manifests/reviewed_manifest_v1.csv`
- Dry-run output:
  `Google Colab/Fundus DR Hem Exudate Separation/review_manifests/proposed_fitting_manifest_v1/fitting_manifest_v1_dry_run.csv`
- Design reference:
  `Google Colab/Fundus DR Hem Exudate Separation/review_manifests/fitting_manifest_v1_design.md`

## Inclusion Rules

Included accepted classes only:

- `normal_or_non_specific`
- `dr_pattern_dominant`
- `exudate_macular_pattern_dominant`
- `mixed_hemorrhage_exudate_pattern`

Excluded:

- `hemorrhage_pattern_dominant_non_dr`
- `unusable_low_quality`
- `needs_second_review`
- non-accepted rows

## Deterministic Selection Rule

For each included class:

- select only `review_status = accepted`
- sort deterministically by `source_batch`, then `source_row_id`, then
  `evidence_id`
- cap at 466 rows

Within each capped class, assign splits in deterministic order:

- first 326 rows -> `train`
- next 70 rows -> `val`
- final 70 rows -> `test`

## Dry-Run Counts

- Dry-run row count: 1864
- Class counts:
  - `normal_or_non_specific`: 466
  - `dr_pattern_dominant`: 466
  - `exudate_macular_pattern_dominant`: 466
  - `mixed_hemorrhage_exudate_pattern`: 466
- Split counts:
  - `train`: 1304
  - `val`: 280
  - `test`: 280

## Verification

- `evidence_id` unique: yes
- `(source_batch, source_row_id)` unique: yes
- `review_status = accepted` for all dry-run rows: yes
- `hemorrhage_pattern_dominant_non_dr` included: 0
- `unusable_low_quality` included: 0
- unresolved rows included: 0
- `reviewed_manifest_v1.csv` unchanged at 2955 rows: yes
- `fitting_manifest_v1.csv` remains absent: yes
- `challenge_manifest_v1.csv` remains absent: yes

## Safety Statement

- No canonical fitting manifest was created.
- No challenge manifest was created.
- No training was performed.
- No fitting was performed.
- No model/app/backend/runtime files were changed.
- No preserved package files were changed.
