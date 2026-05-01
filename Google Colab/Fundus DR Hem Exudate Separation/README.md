# Google Colab Fundus DR Hem Exudate Separation

This folder is the initial Colab scaffold for the future EyeScan training lane:

- `fundus_dr_hem_exudate_separation_v1`

This is planning and notebook scaffolding only. It is not a production model,
does not approve training, and must not replace any preserved baseline package.

## Baseline Preservation

Preserved baselines remain unchanged:

- `anterior_boundary_v1_efficientnetb0_colab_package.zip`
- `fundus_broad_abnormality_v1_efficientnetb0_colab_package.zip`

Comparison-only evidence remains comparison-only:

- `anterior_boundary_v1_efficientnetb0_colab_package (1).zip`
- `fundus_broad_abnormality_v1_efficientnetb2_colab_package.zip`

This lane must not modify Flutter code, backend inference code, model loading
logic, arbitration logic, deployment files, or preserved model packages.

## Objective

The goal is to plan a future comparison/evaluation-only fundus specialist that
improves separation between:

- diabetic-retinopathy-like fundus patterns
- hemorrhage-dominant non-DR vascular patterns
- exudate or macular-dominant patterns
- mixed hemorrhage/exudate patterns
- normal or non-specific fundus images

The first planned architecture is EfficientNetB0.

## Five-Class Design

Planned labels:

- `normal_or_non_specific`
- `dr_pattern_dominant`
- `hemorrhage_pattern_dominant_non_dr`
- `exudate_macular_pattern_dominant`
- `mixed_hemorrhage_exudate_pattern`

The planned label order is:

```json
{
  "normal_or_non_specific": 0,
  "dr_pattern_dominant": 1,
  "hemorrhage_pattern_dominant_non_dr": 2,
  "exudate_macular_pattern_dominant": 3,
  "mixed_hemorrhage_exudate_pattern": 4
}
```

## Mixed-Class Reason

Hemorrhages and exudates often co-occur in real fundus images, especially in
diabetic retinopathy and vascular disease. The mixed class is included to
reduce unstable forced labels when both hemorrhage and exudate are prominent
and neither pattern clearly dominates.

The mixed class should not become a catch-all for unclear, low-quality, or
non-specific images.

## Dataset Rules

Include only reviewed or source-mapped fundus images that can support this
five-class taxonomy.

Possible future sources:

- reviewed broad-abnormality curation rows relabeled into this five-class task
- DR datasets reviewed for DR-pattern dominance versus focal lesion dominance
- non-DR vascular examples for `hemorrhage_pattern_dominant_non_dr`
- exudate or macular-focused examples
- clean fundus controls and non-specific hard negatives
- a fixed challenge set kept outside model fitting

Exclude:

- non-fundus, anterior-eye, screenshot, or wrong-mode images unless used in a
  separate quality task
- low-quality images where lesion pattern cannot be assessed reliably
- rows marked `exclude`, `needs_second_review`, or `challenge_only`
- unreviewed broad disease labels that do not support the pattern taxonomy
- duplicate image paths unless a deterministic policy is documented
- challenge-set images from train/validation/test fitting

If a case cannot be separated reliably between two lesion-pattern labels, do
not force it into training. Defer it for second review or challenge-only use.

## Evaluation Criteria

Raw accuracy is not the primary metric.

Primary review metrics:

- macro F1
- per-class recall
- per-class precision where false positives matter
- confusion matrix review
- fixed challenge-set review, when available

Required confusion reviews:

- `dr_pattern_dominant` versus `hemorrhage_pattern_dominant_non_dr`
- `exudate_macular_pattern_dominant` versus
  `mixed_hemorrhage_exudate_pattern`
- whether the mixed class reduces unstable forced predictions compared with a
  four-class structure

## Package Naming

Primary future package name:

- `fundus_dr_hem_exudate_separation_v1_efficientnetb0_colab_package.zip`

Optional future B2 comparison package:

- `fundus_dr_hem_exudate_separation_v1_efficientnetb2_colab_package.zip`

EfficientNetB2 is comparison-only and must use the same manifest, splits,
augmentation, class weighting, and evaluation protocol as the EfficientNetB0
run.

## Expected Future Outputs

A future package should include:

- `classification_report.txt`
- `confusion_matrix.png`
- `per_class_metrics.csv`
- `sample_predictions.csv`
- `misclassified_examples/`
- `training_curves.png`
- `README.md`
- `manifest.json`
- `labels.txt`
- `model.tflite`

The notebook in this folder is scaffold-only and should not create these
outputs until training is explicitly approved later.
