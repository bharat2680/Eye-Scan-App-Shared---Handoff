# Challenge Manifest v1 Design

This document defines a proposed design for `challenge_manifest_v1.csv`.
It is a design artifact only. The canonical challenge manifest is not created
by this note.

## Purpose

`challenge_manifest_v1` is intended for stress-testing and evaluation only.
It should collect difficult, ambiguous, or model-disagreement examples that
probe known weaknesses in the Fundus DR evidence lane.

It is not intended for:

- training
- fitting
- app/backend/runtime integration
- model promotion
- production approval
- clinical claims

The challenge set should answer a narrow question: can a candidate model handle
known difficult boundary cases better than the current reference baseline?

## Candidate Sources

Potential sources for a future dry-run challenge manifest include:

- Round 1 error-slice rows marked `keep_label_model_wrong`
- Round 1 rows marked `downgrade_needs_second_review`
- Round 1 rows marked `unusable_low_quality`, as quality stress cases only
- persistent confusion cases from Baselines 001, 002, and 003
- held-out rows from `fitting_manifest_v1.csv` or `fitting_manifest_v2.csv`, if
  they are useful and traceable
- future manually reviewed difficult cases

The first dry-run should favor rows with strong traceability back to the
Round 1 error-slice review package and baseline prediction exports.

## Exclusion Boundaries

Challenge rows must not blur the line between stress evaluation and accepted
training evidence.

- Do not include unresolved labels as accepted disease truth.
- Do not use challenge rows for training.
- Do not mix challenge rows into `fitting_manifest_v1.csv` or
  `fitting_manifest_v2.csv`.
- Do not treat quality or unusable rows as disease labels.
- Quality and unusable rows must be marked as quality/exclusion stress cases.
- Do not promote rows from challenge status into canonical manifests without a
  separate reviewed correction process.

## Proposed Challenge Categories

Use explicit challenge categories so evaluation failures are interpretable:

- `subtle_dr_missed_as_normal`
- `exudate_vs_mixed_boundary`
- `mixed_vs_dr_boundary`
- `mixed_vs_exudate_boundary`
- `low_quality_or_low_contrast`
- `model_disagreement`
- `needs_second_review_boundary`

Rows may later need one primary category plus a short reason rather than
multiple categories, so challenge-set slices remain easy to audit.

## Proposed Schema

Proposed columns:

- `challenge_id`
- `evidence_id`
- `source_manifest`
- `source_batch`
- `source_row_id`
- `image_path`
- `resolved_external_path_optional`
- `original_review_bucket`
- `fitting_class_if_any`
- `challenge_category`
- `challenge_reason`
- `baseline_001_prediction`
- `baseline_002_prediction`
- `baseline_003_prediction`
- `review_action`
- `expected_handling`
- `include_for_challenge`
- `notes`

Column intent:

- `challenge_id`: stable challenge row identifier, independent of source row
  order.
- `evidence_id`: original evidence identifier for traceability.
- `source_manifest`: source file or package where the row was drawn from.
- `source_batch` and `source_row_id`: source provenance where available.
- `image_path`: original manifest image path.
- `resolved_external_path_optional`: local Windows/Mac/Colab resolved path when
  useful for local evaluation, but not required for canonical portability.
- `original_review_bucket`: existing reviewed bucket before challenge grouping.
- `fitting_class_if_any`: class used in a fitting manifest, if the row was part
  of one.
- `challenge_category`: primary stress-test category.
- `challenge_reason`: human-readable reason the row belongs in the challenge
  set.
- `baseline_001_prediction`, `baseline_002_prediction`,
  `baseline_003_prediction`: prediction provenance where available.
- `review_action`: manual review support action, if the row comes from a
  reviewed error slice.
- `expected_handling`: evaluation expectation, such as correct boundary class,
  second-review flag, or quality rejection.
- `include_for_challenge`: explicit yes/no inclusion switch for dry-run review.
- `notes`: reviewer or audit notes.

## Recommended First Dry-Run

Do not create canonical `challenge_manifest_v1.csv` yet.

The recommended next artifact is `challenge_manifest_v1_dry_run.csv`, derived
from the Round 1 proposed corrections and error-slice rows. The first dry-run
should be small, traceable, and reviewable before it becomes canonical.

Recommended first dry-run source:

- `training/fundus_dr_fitting_v1_baseline_scaffold/error_slices/round1_proposed_corrections/`
- `training/fundus_dr_fitting_v1_baseline_scaffold/error_slices/visual_review_pack/`
- per-row baseline prediction exports where available, especially the
  Baseline 003 v2 val/test export

Suggested first dry-run composition:

- rows marked `keep_label_model_wrong` where a baseline made a persistent error
- rows marked `downgrade_needs_second_review` as boundary/ambiguity stress
  examples
- a small subset of `unusable_low_quality` rows as quality stress cases only
- repeated Baseline 001/002/003 confusion patterns around exudate, mixed, and
  DR-pattern boundaries

Keep the dry-run separate from training manifests. Review and approve the
dry-run before creating canonical `challenge_manifest_v1.csv`.

## Safety

This design is evaluation-only.

- no training is performed
- no fitting execution is performed
- no model files are created
- no TFLite export is approved
- no app/backend/runtime integration is approved
- no model promotion is approved
- no production claim is made
- `reviewed_manifest_v1.csv` remains unchanged
- `fitting_manifest_v1.csv` remains unchanged
- `fitting_manifest_v2.csv` remains unchanged
- `challenge_manifest_v1.csv` remains absent
