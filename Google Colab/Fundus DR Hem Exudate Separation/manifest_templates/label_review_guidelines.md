# Fundus DR Hem Exudate Separation V1 Label Review Guidelines

These guidelines support future dataset review for
`fundus_dr_hem_exudate_separation_v1`.

They are planning documentation only. Do not start training from these files.
Do not create model artifacts. Do not replace preserved baseline packages.

## Five-Class Labels

Use exactly these labels for `final_label`:

- `normal_or_non_specific`
- `dr_pattern_dominant`
- `hemorrhage_pattern_dominant_non_dr`
- `exudate_macular_pattern_dominant`
- `mixed_hemorrhage_exudate_pattern`

## General Review Flow

1. Add each candidate row with `review_status` set to `unreviewed`.
2. Fill `proposed_label` only as a source-mapping hint.
3. Leave `final_label` empty until image-level review is complete.
4. After review, set `final_label` only when the visible pattern fits one of
   the five labels with enough confidence.
5. Set `review_status` to `accepted` only when the row is eligible for future
   train/val/test fitting.
6. Use `needs_second_review` for boundary, low-confidence, or clinically
   ambiguous cases.
7. Use `excluded` for unusable rows and fill `exclude_reason`.
8. Use `challenge_only` for fixed held-out examples that must not enter model
   fitting.

Training must use `final_label` only. It must not use `proposed_label`.

## Label Guidance

### `normal_or_non_specific`

Use for clean healthy fundus images or images with no reliable visible
pathology above the image/noise threshold.

Use this when:

- the fundus appears clean or non-specific
- visible abnormalities are too weak or unreliable to support a lesion-pattern
  label
- the row is a hard negative but still acceptable quality fundus imagery

Do not use this for low-quality images where the retina cannot be assessed.
Low-quality rows should be excluded or routed to second review.

### `dr_pattern_dominant`

Use when the overall lesion distribution is most consistent with a
diabetic-retinopathy-like pattern.

Typical cues may include:

- microaneurysm-like or dot/blot hemorrhage patterns
- exudates in a broader DR-like distribution
- multifocal posterior-pole or retinal lesion pattern where the whole pattern
  matters more than one isolated lesion type

Do not use only because the source dataset says DR. The image-level pattern
must support the label.

### `hemorrhage_pattern_dominant_non_dr`

Use for hemorrhage-dominant images where the distribution suggests a non-DR
vascular pattern.

Typical cues may include:

- sectoral hemorrhage pattern
- flame-shaped hemorrhage pattern
- vein-occlusion-like appearance
- hypertensive-retinopathy-like appearance
- hemorrhage-dominant pattern with exudates absent or clearly secondary

This is the highest sourcing-risk class. If clean examples cannot be sourced,
mark the class as pending or underpowered instead of forcing weak examples into
it.

### `exudate_macular_pattern_dominant`

Use for hard exudate or lipid-dominant images, especially when the visible
pattern is macular, circinate, or macular-star-like.

Use this when exudate/lipid is the dominant visual finding and hemorrhage is
absent, minor, or secondary.

Do not use this for mixed cases where hemorrhage and exudate are both prominent
and neither dominates.

### `mixed_hemorrhage_exudate_pattern`

Use only when hemorrhage and exudate are both prominent and neither pattern
clearly dominates.

This class exists to reduce unstable forced labels between DR-like,
hemorrhage-dominant, and exudate-dominant cases.

Do not use this as:

- a vague catch-all
- a substitute for `needs_second_review`
- a place for low-quality images
- a place for normal or non-specific images

If the case is unclear because image quality is poor, do not assign the mixed
class. Use `needs_second_review` or exclude the row.

## Challenge-Only Handling

Challenge examples are for fixed held-out review only.

For challenge rows:

- set `split` to `challenge`
- set `review_status` to `challenge_only`
- set `challenge_only` to `true`
- keep them out of train/val/test fitting

Challenge examples should cover common boundary cases and known confusion
risks.

## Duplicate Handling

Use `duplicate_group_id` to group duplicate or near-duplicate images.

Before future training export:

- choose at most one representative per duplicate group for fitting unless
  there is an explicit reason to keep more
- keep duplicates from leaking across train/val/test
- document excluded duplicates with `exclude_reason`

## Dataset Sourcing Checklist

Before a future training pass, collect and review:

- DR-pattern examples: multifocal DR-like lesion distribution, including cases
  with hemorrhages and/or exudates in a DR-like pattern.
- Non-DR hemorrhage examples: sectoral, flame, blot, vein-occlusion-like, or
  hypertensive-retinopathy-like hemorrhage-dominant examples.
- Exudate/macular examples: hard exudate, lipid, circinate, macular, or
  macular-star-like examples where exudate is dominant.
- Mixed hemorrhage/exudate examples: cases where hemorrhage and exudate are
  both prominent and neither clearly dominates.
- Clean normal/non-specific examples: healthy or no-reliable-pathology fundus
  images with adequate image quality.
- Held-out challenge examples: fixed boundary cases for DR versus non-DR
  hemorrhage, exudate versus mixed, normal hard negatives, and underpowered
  class review.

## Review Quality Bar

Do not force labels for:

- poor field or partial retina visibility
- severe blur, glare, compression artifact, or media opacity
- non-fundus or wrong-mode images
- source labels without image-level confirmation
- ambiguous lesion patterns where the intended class cannot be defended

Use `needs_second_review`, `excluded`, or `challenge_only` instead.
