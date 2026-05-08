# Baseline 001 vs Baseline 002 Comparison

This note compares the first two evaluation-only Fundus DR fitting v1
baselines.

- Baseline 001: EfficientNetB0, ImageNet initialization, frozen backbone.
- Baseline 002: same manifest and splits, EfficientNetB0, frozen warmup, then
  top-block fine-tuning at low learning rate.

Neither baseline is approved for app integration, model promotion, TFLite
export, production use, or clinical claims.

## Overall Metric Comparison

| metric | Baseline 001 | Baseline 002 | Delta |
| --- | ---: | ---: | ---: |
| validation accuracy | 0.7071 | 0.7071 | 0.0000 |
| validation macro F1 | 0.7043 | 0.7067 | +0.0023 |
| validation weighted F1 | 0.7043 | 0.7067 | +0.0023 |
| test accuracy | 0.7143 | 0.7107 | -0.0036 |
| test macro F1 | 0.7089 | 0.7078 | -0.0011 |
| test weighted F1 | 0.7089 | 0.7078 | -0.0011 |

Baseline 002 did not materially improve over Baseline 001. The validation macro
F1 improvement is very small, while held-out test accuracy and test macro F1 are
slightly lower.

Both runs avoided class collapse.

## Class-Wise Test Comparison

| class | B001 precision | B001 recall | B001 F1 | B002 precision | B002 recall | B002 F1 | F1 delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `normal_or_non_specific` | 0.7875 | 0.9000 | 0.8400 | 0.8676 | 0.8429 | 0.8551 | +0.0151 |
| `dr_pattern_dominant` | 0.6786 | 0.8143 | 0.7403 | 0.6186 | 0.8571 | 0.7186 | -0.0217 |
| `exudate_macular_pattern_dominant` | 0.8125 | 0.5571 | 0.6610 | 0.7778 | 0.6000 | 0.6774 | +0.0164 |
| `mixed_hemorrhage_exudate_pattern` | 0.6029 | 0.5857 | 0.5942 | 0.6230 | 0.5429 | 0.5802 | -0.0141 |

Baseline 002 shifted behavior rather than clearly improving it.

- `normal_or_non_specific` improved modestly on F1.
- `dr_pattern_dominant` recall improved, but precision dropped enough that F1
  declined.
- `exudate_macular_pattern_dominant` recall improved from `0.5571` to `0.6000`,
  but precision declined.
- `mixed_hemorrhage_exudate_pattern` remained the weakest class and declined
  slightly on F1.

## Confusion Comparison

Baseline 001 test confusion matrix:

| true class | normal | dr_pattern | exudate | mixed |
| --- | ---: | ---: | ---: | ---: |
| `normal_or_non_specific` | 63 | 4 | 0 | 3 |
| `dr_pattern_dominant` | 7 | 57 | 2 | 4 |
| `exudate_macular_pattern_dominant` | 6 | 5 | 39 | 20 |
| `mixed_hemorrhage_exudate_pattern` | 4 | 18 | 7 | 41 |

Baseline 002 test confusion matrix:

| true class | normal | dr_pattern | exudate | mixed |
| --- | ---: | ---: | ---: | ---: |
| `normal_or_non_specific` | 59 | 7 | 1 | 3 |
| `dr_pattern_dominant` | 5 | 60 | 4 | 1 |
| `exudate_macular_pattern_dominant` | 1 | 8 | 42 | 19 |
| `mixed_hemorrhage_exudate_pattern` | 3 | 22 | 7 | 38 |

Key confusion pairs:

| confusion pair | Baseline 001 | Baseline 002 | Change |
| --- | ---: | ---: | ---: |
| `exudate_macular_pattern_dominant -> mixed_hemorrhage_exudate_pattern` | 20 | 19 | -1 |
| `mixed_hemorrhage_exudate_pattern -> dr_pattern_dominant` | 18 | 22 | +4 |

The top-block fine-tuning did not solve the main confusion boundary. It slightly
reduced exudate-to-mixed confusion, but increased mixed-to-DR confusion.

Other notable movement:

- `dr_pattern_dominant -> mixed_hemorrhage_exudate_pattern` improved from `4`
  to `1`.
- `normal_or_non_specific -> dr_pattern_dominant` worsened from `4` to `7`.
- `exudate_macular_pattern_dominant -> dr_pattern_dominant` worsened from `5`
  to `8`.

## Interpretation

Baseline 002 does not provide enough improvement to replace Baseline 001 as the
reference baseline. It behaves like a near tie: a tiny validation macro F1 gain,
a slight test macro F1 decline, and the same main error families.

The top-block fine-tuning experiment suggests the bottleneck is not just
"unfreeze a little more." The remaining issue likely needs one or more of:

- data and label-boundary review for mixed, exudate-dominant, and DR-pattern
  cases
- targeted review of the highest-confusion error slices
- higher-resolution or lesion-aware strategy
- clearer handling of broad mixed-pattern evidence labels

Another blind fine-tuning run is not the safest next step.

## Recommendation

Keep Baseline 001 as the current reference baseline.

Do not:

- promote either model
- export TFLite
- integrate either model into app/backend/runtime
- make production claims
- start a broad hyperparameter sweep

Next safe lane:

- error-slice review of mixed/exudate/DR confusion cases

The most useful next artifact would be a review pack or audit table focused on
false `exudate_macular_pattern_dominant -> mixed_hemorrhage_exudate_pattern`
and false `mixed_hemorrhage_exudate_pattern -> dr_pattern_dominant` cases from
the held-out test split.

## Safety Statement

Both baselines are evaluation-only.

- no production claim is made
- no app integration is approved
- no model promotion is approved
- no TFLite export is approved
