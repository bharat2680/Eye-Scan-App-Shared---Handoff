# Fundus DR Hemorrhage Exudate Separation V1 Plan

## Status

This is a future planning scaffold only.

Do not treat this lane as production, do not start training from this document
alone, and do not replace any preserved model baseline.

Current preserved baselines remain:

- `anterior_boundary_v1_efficientnetb0_colab_package.zip`
- `fundus_broad_abnormality_v1_efficientnetb0_colab_package.zip`

Current comparison-only evidence remains:

- `anterior_boundary_v1_efficientnetb0_colab_package (1).zip`
- `fundus_broad_abnormality_v1_efficientnetb2_colab_package.zip`

This lane must not modify Flutter code, backend inference code, model loading
logic, arbitration logic, deployment files, or preserved package artifacts.

## Lane Objective

Lane name:

- `fundus_dr_hem_exudate_separation_v1`

Primary planned run:

- `fundus_dr_hem_exudate_separation_v1_efficientnetb0_colab`

Primary planned package:

- `fundus_dr_hem_exudate_separation_v1_efficientnetb0_colab_package.zip`

Objective:

Create a future comparison/evaluation-only fundus specialist that improves
separation between diabetic-retinopathy-like fundus patterns, non-DR
hemorrhage-dominant vascular patterns, exudate or macular-dominant patterns,
mixed hemorrhage/exudate patterns, and normal or non-specific fundus images.

The current narrowed 4-class fundus broad-abnormality baseline remains the
source of truth for preserved baseline status. This new lane is a refinement
candidate only and must not be promoted by naming, packaging, or runtime wiring
without a later explicit review.

## Five-Class Definitions

| Label | Definition | Intended use |
| --- | --- | --- |
| `normal_or_non_specific` | Clean healthy fundus or no reliable visible pathology above image/noise threshold. | Normal controls, uncertain low-signal non-specific images, and images where visible findings are not strong enough for a lesion-pattern label. |
| `dr_pattern_dominant` | Fundus images where the overall pattern is most consistent with diabetic-retinopathy-like distribution, including microaneurysms, dot/blot hemorrhages, and/or exudates in a DR-like pattern. | DR-like global or multifocal lesion pattern, especially when the total distribution matters more than one isolated lesion type. |
| `hemorrhage_pattern_dominant_non_dr` | Hemorrhage-dominant images where the distribution suggests non-DR vascular patterns such as sectoral, flame, blot, vein-occlusion-like, or hypertensive-retinopathy-like appearance. | Non-DR hemorrhage-heavy vascular patterns and hard negatives for DR-like classification. |
| `exudate_macular_pattern_dominant` | Hard exudate or lipid-dominant images, especially macular, circinate, or macular-star-like patterns. | Exudate/macular-dominant cases where hemorrhage is absent, minor, or not the dominant visual pattern. |
| `mixed_hemorrhage_exudate_pattern` | Images where hemorrhage and exudate are both prominent and neither pattern clearly dominates. | Boundary cases that would otherwise create forced-label noise between DR-like, hemorrhage-dominant, and exudate-dominant labels. |

## Dataset Inclusion Rules

Include only fundus images that have been manually reviewed or source-mapped
with enough confidence to support this lane's five-class taxonomy.

Acceptable future sources may include:

- existing reviewed broad-abnormality curation rows after explicit relabeling
  into this five-class taxonomy
- DR datasets with enough image-level review to separate DR-pattern-dominant
  cases from focal exudate or mixed lesion cases
- non-DR vascular datasets or reviewed clinical-style examples for
  `hemorrhage_pattern_dominant_non_dr`
- exudate/macular-focused examples for `exudate_macular_pattern_dominant`
- clean fundus controls and non-specific fundus hard negatives
- a fixed challenge set kept completely outside train/validation/test training
  rows

Each included row should preserve:

- original image path or source identifier
- assigned five-class label
- split
- source dataset
- source label
- cohort or review bucket
- review status
- reviewer notes for boundary cases

## Dataset Exclusion Rules

Exclude from training and validation:

- non-fundus, anterior-eye, screenshot, or wrong-mode images unless they are
  explicitly part of a separate quality/wrong-mode task
- low-quality images where lesion pattern cannot be reliably assessed
- rows marked `exclude`, `needs_second_review`, or `challenge_only`
- duplicate image paths unless the manifest builder has a documented,
  deterministic latest-row-wins policy
- cases where the only available label is broad disease name and the image has
  not been reviewed for this lane's pattern-level taxonomy
- challenge-set examples, which must remain separate from model fitting

If a case cannot be separated reliably between two lesion-pattern labels, it
should not be forced into a training label. Use `needs_second_review`,
`challenge_only`, or defer the image until review consensus exists.

## Label Mapping Strategy

Planned label order:

```json
{
  "normal_or_non_specific": 0,
  "dr_pattern_dominant": 1,
  "hemorrhage_pattern_dominant_non_dr": 2,
  "exudate_macular_pattern_dominant": 3,
  "mixed_hemorrhage_exudate_pattern": 4
}
```

Training code and evaluation notebooks should map labels by string first, not
by stale numeric indices from older manifests.

Any future B0 and B2 comparison must keep the same:

- accepted manifest rows
- train/validation/test split assignment
- image preprocessing
- augmentation policy
- class weighting policy
- evaluation outputs
- challenge-set evaluation process

EfficientNetB0 is the first planned architecture. EfficientNetB2 may be
documented later only as a comparison run against the same curated data and
evaluation protocol.

## Mixed-Class Labelling Rule

Use `mixed_hemorrhage_exudate_pattern` only when hemorrhage and exudate are
both prominent and neither pattern clearly dominates.

Prefer a more specific label when one pattern is clearly dominant:

- use `dr_pattern_dominant` when the overall distribution is DR-like, even if
  both hemorrhages and exudates are present
- use `hemorrhage_pattern_dominant_non_dr` when hemorrhage dominates and the
  distribution appears non-DR vascular, sectoral, flame-shaped,
  vein-occlusion-like, or hypertensive-retinopathy-like
- use `exudate_macular_pattern_dominant` when hard exudate, lipid, circinate,
  macular, or macular-star-like appearance dominates and hemorrhage is absent
  or secondary

The mixed class exists to reduce unstable forced predictions. It should not
become a catch-all for unclear, low-quality, or non-specific images.

## Package Naming Convention

Primary B0 package:

- `fundus_dr_hem_exudate_separation_v1_efficientnetb0_colab_package.zip`

Primary B0 run name:

- `fundus_dr_hem_exudate_separation_v1_efficientnetb0_colab`

Optional future B2 comparison package:

- `fundus_dr_hem_exudate_separation_v1_efficientnetb2_colab_package.zip`

Optional B2 run name:

- `fundus_dr_hem_exudate_separation_v1_efficientnetb2_colab`

The B2 package name must be treated as comparison-only unless a later review
explicitly approves otherwise. Neither B0 nor B2 from this lane should replace
`fundus_broad_abnormality_v1_efficientnetb0_colab_package.zip`.

## Required Evaluation Outputs

Any future package for this lane should include:

- `classification_report.txt`
- `confusion_matrix.png`
- `per_class_metrics.csv`
- `sample_predictions.csv`
- `misclassified_examples/`
- `training_curves.png` including validation loss
- `README.md`
- `manifest.json`
- `labels.txt`
- `model.tflite`

Recommended additional metadata:

- model architecture and input size
- train/validation/test counts by class
- source-dataset counts by class
- class weighting configuration
- augmentation configuration
- random seed
- challenge-set summary, if available

## Promotion And Evaluation Criteria

Raw accuracy must not be the primary metric.

Primary review metrics:

- macro F1
- per-class recall
- per-class precision where false positives are clinically meaningful
- confusion matrix review
- boundary-case review on a fixed challenge set

Required confusion reviews:

- review confusion between `dr_pattern_dominant` and
  `hemorrhage_pattern_dominant_non_dr`
- review confusion between `exudate_macular_pattern_dominant` and
  `mixed_hemorrhage_exudate_pattern`
- review whether `mixed_hemorrhage_exudate_pattern` reduces unstable forced
  predictions compared with a four-class structure

The mixed class should be judged by whether it makes predictions more stable
and clinically honest for co-occurring lesion patterns, not only by headline
recall.

This lane is not eligible for production promotion until:

- every class has enough clean accepted examples for train/validation/test
- `hemorrhage_pattern_dominant_non_dr` has a credible source, or is explicitly
  marked pending/underpowered
- challenge-set images remain held out from fitting
- misclassified examples are manually reviewed
- B0/B2 comparisons, if any, use identical splits and evaluation process
- the preserved broad-abnormality B0 baseline remains unchanged
- a later runtime integration decision is explicitly approved

## Risks And Known Limitations

- Hemorrhages and exudates frequently co-occur in real fundus images, especially
  in diabetic retinopathy and vascular disease.
- `mixed_hemorrhage_exudate_pattern` may reduce forced-label noise, but it may
  also become unstable if used for vague or low-quality images.
- `hemorrhage_pattern_dominant_non_dr` is the highest sourcing risk. If clean
  non-DR vascular examples are not available, this class may need to remain
  pending, underpowered, or excluded from a first training pass.
- DR-source datasets may overrepresent DR labels while still containing focal
  hemorrhage or exudate patterns that need image-level review.
- Exudate/macular-dominant cases may overlap with DR, hypertensive disease, or
  other retinal disease categories, so labels must describe visible pattern,
  not claim final diagnosis.
- The lane is pattern-separation support, not a clinical diagnosis engine.
- Headline performance on tiny or internally curated splits will not be enough
  for promotion.
- Any future package must stay comparison/evaluation-only until separately
  reviewed.
