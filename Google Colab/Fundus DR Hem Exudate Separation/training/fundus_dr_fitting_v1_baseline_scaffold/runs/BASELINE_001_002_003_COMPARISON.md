# Baseline 001/002/003 Comparison

This note compares the first three evaluation-only Fundus DR fitting baselines.

- Baseline 001: `fitting_manifest_v1.csv`, EfficientNetB0, ImageNet initialization, frozen backbone.
- Baseline 002: `fitting_manifest_v1.csv`, EfficientNetB0, frozen warmup, then top-block fine-tuning.
- Baseline 003: `fitting_manifest_v2.csv`, EfficientNetB0, ImageNet initialization, frozen backbone.

No baseline is approved for app/backend/runtime integration, model promotion,
TFLite export, production use, or clinical claims.

## Overall Metric Comparison

| metric | Baseline 001 | Baseline 002 | Baseline 003 v2 |
| --- | ---: | ---: | ---: |
| manifest | `fitting_manifest_v1` | `fitting_manifest_v1` | `fitting_manifest_v2` |
| train rows | 1304 | 1304 | 1184 |
| val rows | 280 | 280 | 256 |
| test rows | 280 | 280 | 256 |
| epochs run | 14 | 14 | 5 |
| best validation epoch | 9 | 9 | 3 |
| validation accuracy | 0.7071 | 0.7071 | 0.7031 |
| validation macro F1 | 0.7043 | 0.7067 | 0.7054 |
| validation weighted F1 | 0.7043 | 0.7067 | 0.7054 |
| test accuracy | 0.7143 | 0.7107 | 0.6523 |
| test macro F1 | 0.7089 | 0.7078 | 0.6528 |
| test weighted F1 | 0.7089 | 0.7078 | 0.6528 |
| class collapse observed | no | no | no |

Baseline 001 remains the current reference baseline. Baseline 002 did not
materially improve over Baseline 001. Baseline 003 underperformed both earlier
runs on held-out test macro F1, although the result must be interpreted with
the important caveat that it stopped by execution timeout after epoch 5 and was
finalized from the best validation checkpoint at epoch 3.

## Data Manifest Comparison

Baselines 001 and 002 used `fitting_manifest_v1.csv`:

- total rows: 1864
- train rows: 1304
- validation rows: 280
- test rows: 280
- balanced class count: 466 per class

Baseline 003 used `fitting_manifest_v2.csv`:

- total rows: 1696
- train rows: 1184
- validation rows: 256
- test rows: 256
- balanced class count: 424 per class

The v2 manifest is cleaner and smaller because Round 1 error-slice review held
out ambiguous, low-quality, and unassigned rows and corrected proposed label
boundary rows. Cleaner labels did not automatically improve this quick frozen
backbone baseline.

## Training Setup Comparison

| setup | Baseline 001 | Baseline 002 | Baseline 003 v2 |
| --- | --- | --- | --- |
| model | EfficientNetB0 | EfficientNetB0 | EfficientNetB0 |
| initialization | ImageNet | ImageNet | ImageNet |
| image size | 224x224 | 224x224 | 224x224 |
| backbone | frozen | warmup frozen, then top block unfrozen | frozen |
| training recipe | classifier head only | classifier head warmup plus top-block fine-tuning | classifier head only |
| manifest | v1 | v1 | v2 |
| stop reason | early stopping patience | early stopping patience | execution timeout after epoch 5 |

Baseline 003 intentionally returned to the simpler Baseline 001-style setup to
isolate the data effect of `fitting_manifest_v2.csv` before changing the model
recipe again.

## Class-Wise Test Comparison

| class | B001 F1 | B002 F1 | B003 v2 F1 |
| --- | ---: | ---: | ---: |
| `normal_or_non_specific` | 0.8400 | 0.8551 | 0.7143 |
| `dr_pattern_dominant` | 0.7403 | 0.7186 | 0.6933 |
| `exudate_macular_pattern_dominant` | 0.6610 | 0.6774 | 0.6387 |
| `mixed_hemorrhage_exudate_pattern` | 0.5942 | 0.5802 | 0.5649 |

Baseline 003 did not improve the weakest boundary classes. The mixed class
remained weakest, and normal also declined on the v2 test split.

## Confusion Comparison

Key test confusion pairs:

| confusion pair | Baseline 001 | Baseline 002 | Baseline 003 v2 |
| --- | ---: | ---: | ---: |
| `exudate_macular_pattern_dominant -> mixed_hemorrhage_exudate_pattern` | 20 | 19 | 16 |
| `mixed_hemorrhage_exudate_pattern -> dr_pattern_dominant` | 18 | 22 | 15 |
| `mixed_hemorrhage_exudate_pattern -> exudate_macular_pattern_dominant` | 7 | 7 | 10 |
| `dr_pattern_dominant -> normal_or_non_specific` | 7 | 5 | 3 |
| `normal_or_non_specific -> dr_pattern_dominant` | 4 | 7 | 12 |

Persistent error families remain around the exudate, mixed, and DR-pattern
boundaries. Baseline 003 reduced some raw counts because the v2 test split is
smaller, but it did not remove the same visual boundary problem. It also
introduced a larger `normal_or_non_specific -> dr_pattern_dominant` confusion
count on the v2 test split.

No class collapse occurred in any of the three runs.

## Interpretation

Baseline 001 is still the best reference point by held-out test macro F1.
Baseline 002 shifted class behavior but did not materially improve the result.
Baseline 003 tested the cleaner and smaller v2 data, but the quick frozen
backbone run did not beat the v1 reference. The timeout-limited Baseline 003
run should be treated as an incomplete evaluation, not as a final statement
about the v2 manifest.

The most likely lesson is that data cleanup alone is not enough for this model
recipe at 224x224. The exudate, mixed, and DR-pattern boundaries still need
more explicit evidence design before another broad training attempt.

## Recommendation

Keep Baseline 001 as the current reference baseline.

Do not:

- promote any baseline
- export TFLite
- integrate any baseline into app/backend/runtime
- make production claims
- run a blind Baseline 004

Next safer lane:

- design `challenge_manifest_v1.csv` from held-out, error-slice, and
  needs-second-review rows, or
- perform further manual review of the remaining ambiguous label-boundary cases
  before more training.

Baseline 004 should wait until the challenge design or further manual review
clarifies what the next experiment is meant to prove.

## Safety Statement

These baselines are evaluation-only.

- no production claim is made
- no app integration is approved
- no model promotion is approved
- no TFLite export is approved
- `reviewed_manifest_v1.csv` is not changed
- `fitting_manifest_v1.csv` is not changed
- `fitting_manifest_v2.csv` is not changed
- `challenge_manifest_v1.csv` remains absent
