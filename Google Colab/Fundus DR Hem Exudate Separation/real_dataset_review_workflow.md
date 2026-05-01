# Fundus DR Hem Exudate Separation V1 Real Dataset Review Workflow

## Purpose

This document describes the next safe phase after the starter manifest sample
for `fundus_dr_hem_exudate_separation_v1`.

It prepares a real dataset review workflow only. It does not create a reviewed
manifest, does not create a fitting manifest, does not approve training, and
does not create model artifacts.

The goal is to define how candidate image paths can later move from source
folders into reviewed manifest rows for the five-class fundus pattern-separation
lane.

## Safety Rules

Preserved baselines remain untouched:

- `anterior_boundary_v1_efficientnetb0_colab_package.zip`
- `fundus_broad_abnormality_v1_efficientnetb0_colab_package.zip`

Comparison-only evidence remains comparison-only:

- `anterior_boundary_v1_efficientnetb0_colab_package (1).zip`
- `fundus_broad_abnormality_v1_efficientnetb2_colab_package.zip`

Rules for this lane:

- Do not use source labels directly for training.
- Training may only use reviewed `final_label`.
- `proposed_label` is only a hint.
- Rows with `review_status` of `challenge_only`, `excluded`,
  `needs_second_review`, or `unreviewed` must not enter fitting.
- Rows with `challenge_only == true` must not enter fitting.
- Preserved baseline packages must remain untouched.
- This workflow must not modify runtime app code, backend inference code, model
  loading logic, Colab training logic, deployment files, or package artifacts.

## Review Workflow

1. Collect candidate image paths from selected source folders.
2. Create candidate manifest rows using the approved schema.
3. Fill `source_dataset` with the source collection name.
4. Fill `source_label` with the original folder, file, grade, or dataset label.
5. Optionally fill `proposed_label` as a source-mapping or reviewer-queue hint.
6. Leave `final_label` empty at first.
7. Set `review_status` to `unreviewed`.
8. Set `split` to `unset`.
9. Set `challenge_only` to `false` unless the row is intentionally held out.
10. Manually review each image.
11. Set `review_status` based on image-level review.
12. Assign `final_label` only after the image has been reviewed and accepted.
13. Set `split` only after accepted rows exist and source balance can be
    considered.
14. Keep challenge rows separate from train/validation/test fitting rows.
15. Re-check duplicates, image quality, and source leakage before any future
    fitting export.

## Candidate Manifest Stages

### `raw_candidate_manifest.csv`

Purpose:

- source inventory and review queue only

Expected state:

- `review_status = unreviewed`
- `final_label` empty
- `split = unset`
- `proposed_label` optional

This file is not training-ready.

### `reviewed_manifest_v1.csv`

Purpose:

- reviewer decisions and final labels

Expected state:

- accepted rows have reviewed `final_label`
- second-review rows remain marked `needs_second_review`
- excluded rows remain marked `excluded`
- challenge rows remain marked `challenge_only`

This file is still not automatically training-ready. It is the source of truth
for later export decisions.

### `fitting_manifest_v1.csv`

Purpose:

- future train/validation/test fitting input after review gates pass

Allowed rows:

- `review_status == accepted`
- `challenge_only == false`
- `final_label` is one of the five approved labels
- `split` is `train`, `val`, or `test`
- `image_path` exists in the execution environment
- `exclude_reason` is empty

Do not create this file until a later explicit approval.

### `challenge_manifest_v1.csv`

Purpose:

- fixed held-out boundary and failure-mode review set

Expected state:

- `split = challenge`
- `review_status = challenge_only`
- `challenge_only = true`

Challenge rows must never be used for model fitting.

## Allowed Transition Rules

Allowed review-status transitions:

- `unreviewed` -> `accepted`
- `unreviewed` -> `needs_second_review`
- `unreviewed` -> `excluded`
- `accepted` -> `challenge_only` only if deliberately removed from fitting
- `needs_second_review` -> `accepted` only after second review
- `needs_second_review` -> `excluded`
- `excluded` rows stay excluded unless explicitly restored with review notes

When restoring an excluded row:

- keep prior notes
- add a new explanation in `review_notes`
- clear `exclude_reason` only if the row is genuinely restored
- re-review before assigning or reusing `final_label`

## Class-Specific Review Notes

### `normal_or_non_specific`

Use for clean healthy fundus images or images with no reliable visible
pathology above the image/noise threshold.

Review notes:

- confirm adequate fundus quality and field visibility
- do not use for poor-quality images where pathology cannot be assessed
- avoid treating glaucoma, disc appearance, or source folder names as the
  deciding factor for this lesion-separation lane

### `dr_pattern_dominant`

Use when the overall lesion distribution is most consistent with a
diabetic-retinopathy-like pattern.

Review notes:

- source DR labels are only hints
- confirm the pattern visually before assigning `final_label`
- focal exudate-dominant, focal hemorrhage-dominant, and mixed cases may need
  different labels

### `hemorrhage_pattern_dominant_non_dr`

Use for hemorrhage-dominant images where the distribution suggests a non-DR
vascular pattern.

Review notes:

- this is the highest-risk class for sourcing
- look for sectoral, flame, blot, vein-occlusion-like, or
  hypertensive-retinopathy-like appearances
- do not force DR examples into this class just because hemorrhage is present
- keep unclear examples as `needs_second_review`

### `exudate_macular_pattern_dominant`

Use for hard exudate or lipid-dominant images, especially macular, circinate,
or macular-star-like patterns.

Review notes:

- source disease folders may not map cleanly to this visual pattern
- assign this label only when exudate/macular pattern clearly dominates
- use `mixed_hemorrhage_exudate_pattern` when hemorrhage and exudate are both
  prominent and neither dominates

### `mixed_hemorrhage_exudate_pattern`

Use only when hemorrhage and exudate are both prominent and neither pattern
clearly dominates.

Review notes:

- this class exists to reduce unstable forced labels
- it must not become a vague catch-all
- do not use for low-quality or uncertain images
- if uncertainty comes from image quality or unclear pattern dominance, use
  `needs_second_review`

## Minimum Suggested Starter Target Before Training Discussion

Before any training discussion, aim for at least a small reviewed sample per
class.

There is no exact count requirement yet. The first goal is review quality,
not scale.

Before training is discussed, review:

- whether every class has credible accepted examples
- whether `hemorrhage_pattern_dominant_non_dr` remains underpowered
- whether source diversity is acceptable
- whether class balance is plausible enough for a first experiment
- whether duplicate groups could leak across splits
- whether challenge rows are separated from fitting rows

`hemorrhage_pattern_dominant_non_dr` remains the highest-risk class.

`normal_or_non_specific` and `dr_pattern_dominant` are likely easier to source,
but still require image-level review.

`exudate_macular_pattern_dominant` and
`mixed_hemorrhage_exudate_pattern` need careful boundary review.

## Recommended Reviewer Columns

Use the existing manifest schema:

- `image_path`
- `source_dataset`
- `source_label`
- `proposed_label`
- `final_label`
- `split`
- `review_status`
- `reviewer`
- `review_notes`
- `lesion_pattern_notes`
- `quality_notes`
- `duplicate_group_id`
- `challenge_only`
- `exclude_reason`

## Export Gates

`fitting_manifest_v1.csv` can only include rows where:

- `review_status == accepted`
- `challenge_only == false`
- `final_label` is one of:
  - `normal_or_non_specific`
  - `dr_pattern_dominant`
  - `hemorrhage_pattern_dominant_non_dr`
  - `exudate_macular_pattern_dominant`
  - `mixed_hemorrhage_exudate_pattern`
- `split` is `train`, `val`, or `test`
- `image_path` exists
- `exclude_reason` is empty

Rows must be excluded from fitting export when:

- `review_status == unreviewed`
- `review_status == needs_second_review`
- `review_status == excluded`
- `review_status == challenge_only`
- `challenge_only == true`
- `split == unset`
- `split == challenge`
- `final_label` is empty
- `exclude_reason` is non-empty

## Recommended Next Task

The next safe task after this document is to create a candidate manifest builder
script or notebook helper that scans selected folders and creates
`raw_candidate_manifest.csv` with:

- `final_label` empty
- `review_status = unreviewed`
- `split = unset`
- `challenge_only = false`
- optional `proposed_label` hints based on source mapping

That helper should not train, should not create model artifacts, should not copy
or move datasets, and should not create `fitting_manifest_v1.csv`.
