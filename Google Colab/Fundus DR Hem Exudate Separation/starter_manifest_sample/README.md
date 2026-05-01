# Starter Manifest Sample

This folder contains a tiny schema and review-flow demonstration for
`fundus_dr_hem_exudate_separation_v1`.

It is not training-ready data. Do not use this CSV directly for model fitting,
evaluation, package creation, or baseline comparison.

## Contents

- `starter_manifest_sample.csv`

The CSV uses the exact manifest schema from:

- `../manifest_templates/manifest_template.csv`

All image paths are fake placeholder paths under:

- `datasets/PENDING_REVIEW/`

No datasets were copied or moved to create this sample.

## Review Flow Demonstrated

The five main example rows each show one planned label as `proposed_label`:

- `normal_or_non_specific`
- `dr_pattern_dominant`
- `hemorrhage_pattern_dominant_non_dr`
- `exudate_macular_pattern_dominant`
- `mixed_hemorrhage_exudate_pattern`

`final_label` is intentionally empty for every row. A real manifest must leave
`final_label` empty until a reviewer has performed image-level review and
accepted the row under the five-class taxonomy.

`proposed_label` is only a hint. It may come from source mapping, folder names,
or a reviewer queue, but it must never be used as the training label.

## Safety Rules

- Training export must use `final_label` only.
- Rows with `review_status = unreviewed` must not enter fitting.
- Rows with `review_status = challenge_only` must not enter fitting.
- Rows with `review_status = excluded` must not enter fitting.
- Rows with `challenge_only = true` must not enter train, validation, or test
  fitting.
- Low-quality or uncertain rows must not be forced into a class.
- `mixed_hemorrhage_exudate_pattern` must not be used as a vague catch-all.

## Intended Future Use

This sample should be replaced or copied into a real reviewed manifest later.
Before any training, real candidate rows must be image-reviewed, assigned
`final_label` only after acceptance, checked for duplicates, checked for image
quality, and separated from held-out challenge-only rows.

The next real step should be a small reviewed starter manifest, not training.
