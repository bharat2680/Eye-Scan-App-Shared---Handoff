# Baseline 001 Error Analysis

Baseline 001 was an evaluation-only four-class Fundus DR fitting run using
EfficientNetB0 with ImageNet initialization and a frozen backbone.

No app integration, model promotion, TFLite export, or production claim is
approved from this run.

## Overall Result

- validation accuracy: `0.7071`
- validation macro F1: `0.7043`
- test accuracy: `0.7143`
- test macro F1: `0.7089`
- class collapse observed: `false`

The first baseline is meaningfully above a random four-class baseline and did
not collapse into a single class. It is still evaluation-only and should be
treated as an error-analysis checkpoint rather than a deployable model.

## Class-Wise Interpretation

- `normal_or_non_specific` was the strongest class, with test precision
  `0.7875`, recall `0.9000`, and F1 `0.8400`.
- `dr_pattern_dominant` was decent, with test precision `0.6786`, recall
  `0.8143`, and F1 `0.7403`.
- `exudate_macular_pattern_dominant` had higher precision than recall:
  precision `0.8125`, recall `0.5571`, and F1 `0.6610`. When the model predicts
  this class, it is often right, but it misses many true exudate-dominant rows.
- `mixed_hemorrhage_exudate_pattern` was the weakest class, with test precision
  `0.6029`, recall `0.5857`, and F1 `0.5942`.

This pattern suggests the baseline can identify cleaner normal and DR-pattern
examples, but struggles with visually overlapping lesion patterns.

## Confusion Analysis

Test confusion matrix rows are true classes and columns are predicted classes.

| true class | normal | dr_pattern | exudate | mixed |
| --- | ---: | ---: | ---: | ---: |
| `normal_or_non_specific` | 63 | 4 | 0 | 3 |
| `dr_pattern_dominant` | 7 | 57 | 2 | 4 |
| `exudate_macular_pattern_dominant` | 6 | 5 | 39 | 20 |
| `mixed_hemorrhage_exudate_pattern` | 4 | 18 | 7 | 41 |

Most notable confusion pairs:

- `exudate_macular_pattern_dominant -> mixed_hemorrhage_exudate_pattern`: `20`
- `mixed_hemorrhage_exudate_pattern -> dr_pattern_dominant`: `18`
- `dr_pattern_dominant -> normal_or_non_specific`: `7`
- `mixed_hemorrhage_exudate_pattern -> exudate_macular_pattern_dominant`: `7`
- `exudate_macular_pattern_dominant -> normal_or_non_specific`: `6`

The dominant failure is not simple class collapse. It is boundary confusion
between exudate-dominant, mixed, and DR-pattern evidence.

## Likely Causes

- The label boundary between exudate-dominant and mixed patterns is inherently
  overlapping.
- The mixed bucket may be visually broad, collecting examples with different
  lesion balances and image quality profiles.
- A frozen ImageNet backbone may limit lesion-specific learning, especially for
  small hemorrhages and subtle exudate patterns.
- `224 x 224` resolution may miss fine lesions or reduce the visual separation
  between small exudates and hemorrhage-heavy mixed examples.
- Source labels and review buckets are evidence labels, not clinical diagnoses.
  They are useful for this evidence lane, but they should not be interpreted as
  diagnostic truth.

## Recommended Next Experiment

Run one conservative follow-up only:

- Baseline 002: same manifest, same labels, same fixed splits.
- Keep EfficientNetB0 and `224 x 224` input size.
- Start from ImageNet initialization.
- Use a short warmup with the backbone frozen.
- After warmup, unfreeze only the top EfficientNet block and continue with a low
  learning rate.
- Keep augmentation light and train-only.
- Preserve the same validation/test protocol and report the same metrics.
- Keep outputs outside the repository except small summary artifacts.

The goal of Baseline 002 should be narrow: test whether limited lesion-specific
adaptation improves the exudate/mixed boundary without destabilizing normal and
DR-pattern performance.

## Do Not Recommend

- no app/backend integration
- no model promotion
- no TFLite export
- no production use
- no broad hyperparameter sweep

## Safety Statement

Baseline 001 is evaluation-only.

- no production claim is made
- no app integration is approved
- `reviewed_manifest_v1.csv` remains unchanged
- `fitting_manifest_v1.csv` remains unchanged
- `challenge_manifest_v1.csv` remains absent
