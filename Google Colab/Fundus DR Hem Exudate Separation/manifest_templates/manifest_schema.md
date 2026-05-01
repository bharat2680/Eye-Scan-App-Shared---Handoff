# Fundus DR Hem Exudate Separation V1 Manifest Schema

This manifest schema is for future dataset planning only.

It does not approve training, does not create model artifacts, and does not
replace any preserved baseline package.

Preserved baselines remain:

- `anterior_boundary_v1_efficientnetb0_colab_package.zip`
- `fundus_broad_abnormality_v1_efficientnetb0_colab_package.zip`

## Lane

- lane: `fundus_dr_hem_exudate_separation_v1`
- first planned model: `fundus_dr_hem_exudate_separation_v1_efficientnetb0_colab`
- planned package name:
  `fundus_dr_hem_exudate_separation_v1_efficientnetb0_colab_package.zip`

This lane is comparison/evaluation-only unless a later explicit review says
otherwise.

## Manifest Columns

| Column | Required | Description |
| --- | --- | --- |
| `image_path` | yes | Path to the image in the local or Drive staging environment. |
| `source_dataset` | yes | Source dataset or manual review source. |
| `source_label` | yes | Original source label before EyeScan review. |
| `proposed_label` | no | Optional source-mapped label suggestion. Never use this for training. |
| `final_label` | no until reviewed | Reviewer-approved five-class label. Training may use only this field. |
| `split` | yes | Planned split assignment or staging state. |
| `review_status` | yes | Review lifecycle state. |
| `reviewer` | no | Reviewer name, initials, or review batch identifier. |
| `review_notes` | no | Free-text review notes. |
| `lesion_pattern_notes` | no | Notes about hemorrhage, exudate, DR-like distribution, mixed pattern, or uncertainty. |
| `quality_notes` | no | Image quality, field, media opacity, wrong-mode, or visibility notes. |
| `duplicate_group_id` | no | Shared id for duplicate or near-duplicate images. |
| `challenge_only` | yes | Boolean flag for held-out challenge rows. |
| `exclude_reason` | no | Required when a row is excluded. |

## Allowed Labels

Allowed `final_label` values:

- `normal_or_non_specific`
- `dr_pattern_dominant`
- `hemorrhage_pattern_dominant_non_dr`
- `exudate_macular_pattern_dominant`
- `mixed_hemorrhage_exudate_pattern`

`final_label` should remain empty until the row has been reviewed. The future
training manifest must string-map labels from `final_label`; it must not trust
numeric indices from an older task.

## Allowed Splits

Allowed `split` values:

- `train`
- `val`
- `test`
- `challenge`
- `unset`

Use `unset` for rows still being reviewed or staged. Use `challenge` only for
fixed challenge examples that must remain outside model fitting.

## Allowed Review Statuses

Allowed `review_status` values:

- `unreviewed`
- `accepted`
- `needs_second_review`
- `excluded`
- `challenge_only`

Only rows with `review_status == accepted`, `challenge_only == false`, and
`split` in `train`, `val`, or `test` may be exported into a future fitting
manifest.

Rows with `review_status` of `needs_second_review`, `excluded`, or
`challenge_only` must not enter train/val/test fitting.

## Allowed Challenge Flag Values

Allowed `challenge_only` values:

- `true`
- `false`

Rows with `challenge_only == true` must not enter train/val/test, even if
another column is accidentally set to `train`, `val`, or `test`.

## Export Rules For Future Training

Future manifest export should include only rows where all of these are true:

- `review_status == accepted`
- `challenge_only == false`
- `final_label` is one of the five approved labels
- `split` is `train`, `val`, or `test`
- `image_path` is non-empty and resolves in the execution environment
- the image is not low-quality beyond the lane's review threshold
- the row is not a duplicate selected for exclusion

Future manifest export must exclude rows where any of these are true:

- `review_status == unreviewed`
- `review_status == needs_second_review`
- `review_status == excluded`
- `review_status == challenge_only`
- `challenge_only == true`
- `split == challenge`
- `split == unset`
- `final_label` is empty
- `exclude_reason` is non-empty

## Review Rules

- `proposed_label` may come from source mapping, but training must use
  `final_label` only.
- `final_label` should be empty until a reviewer accepts the row.
- Labels must be string-mapped, not numeric-index-mapped.
- Duplicate or near-duplicate images should share `duplicate_group_id`.
- Low-quality or uncertain rows should not be forced into a class.
- `mixed_hemorrhage_exudate_pattern` must not be used as a vague catch-all.
- Challenge rows must be held out from model fitting and reviewed separately.

## Minimum Future Validation Checks

Before any later training pass, validation should confirm:

- every expected class is present
- minimum count per class is met
- every accepted row has split `train`, `val`, or `test`
- no `challenge_only` row is in train/val/test
- no `needs_second_review` or `excluded` row is in train/val/test
- no accepted row has an empty `final_label`
- duplicate groups have an explicit inclusion/exclusion decision
- missing or corrupt images have been resolved
- output paths cannot overwrite preserved baseline package names
