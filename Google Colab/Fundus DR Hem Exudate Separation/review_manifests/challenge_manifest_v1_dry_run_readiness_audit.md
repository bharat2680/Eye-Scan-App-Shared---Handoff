# Challenge Manifest v1 Dry-Run Readiness Audit

This audit reviews `proposed_challenge_manifest_v1/challenge_manifest_v1_dry_run.csv`
as an evaluation-only stress-test candidate. It does not create canonical
`challenge_manifest_v1.csv`.

## Readiness Recommendation

Do not create canonical `challenge_manifest_v1.csv` yet.

The dry-run structure is traceable and internally deduplicated, but it is not
ready for canonical promotion because 32 dry-run evidence IDs currently overlap
`fitting_manifest_v2.csv` train rows. A challenge set should remain separate
from training data, so the next step is to revise the dry-run or explicitly
sequester those rows from future fitting before creating a canonical challenge
manifest.

## Count Verification

| check | result |
| --- | ---: |
| dry-run rows | 128 |
| duplicate `challenge_id` values | 0 |
| duplicate `evidence_id + challenge_category` pairs | 0 |
| canonical `challenge_manifest_v1.csv` exists | no |
| `reviewed_manifest_v1.csv` rows | 2955 |
| `fitting_manifest_v1.csv` rows | 1864 |
| `fitting_manifest_v2.csv` rows | 1696 |

## Challenge Category Counts

| challenge_category | rows |
| --- | ---: |
| `needs_second_review_boundary` | 50 |
| `label_boundary_correction_candidate` | 35 |
| `exudate_vs_mixed_boundary` | 12 |
| `mixed_vs_dr_boundary` | 12 |
| `mixed_vs_exudate_boundary` | 7 |
| `low_quality_or_low_contrast` | 6 |
| `subtle_dr_missed_as_normal` | 5 |
| `model_disagreement` | 1 |

The categories focus on known model weaknesses from Baselines 001, 002, and
003: subtle DR missed as normal, exudate/mixed boundaries, mixed/DR boundaries,
low-quality cases, model disagreement, and second-review ambiguity.

## Review Action Counts

| review_action | rows |
| --- | ---: |
| `downgrade_needs_second_review` | 50 |
| `keep_label_model_wrong` | 36 |
| `relabel_to_predicted` | 35 |
| `unusable_low_quality` | 6 |
| `unassigned` | 1 |

Rows marked `downgrade_needs_second_review`, `unusable_low_quality`, or
`unassigned` must not be treated as accepted disease truth. They are challenge
or quality-stress candidates only.

## Expected Handling Counts

| expected_handling | rows |
| --- | ---: |
| `flag_for_second_review_not_training` | 50 |
| `model_should_match_original_review_bucket` | 36 |
| `label_boundary_candidate_requires_review` | 35 |
| `quality_stress_case_not_disease_truth` | 6 |
| `review_hold_before_canonical_use` | 1 |

These handling labels make the dry-run suitable for evaluation planning, not
for training or fitting.

## Training-Overlap Audit

The dry-run is not itself a training manifest and should not be used as
training data. However, challenge candidates must also be checked against
current fitting manifests before canonical promotion.

| fitting manifest | overlapping dry-run evidence IDs | split detail | train overlap |
| --- | ---: | --- | ---: |
| `fitting_manifest_v1.csv` | 108 | `val`: 50, `test`: 58 | 0 |
| `fitting_manifest_v2.csv` | 48 | `train`: 32, `val`: 7, `test`: 9 | 32 |

The `fitting_manifest_v2.csv` train overlap is a readiness blocker. Among those
32 overlapping evidence IDs, the dry-run contains 38 challenge rows because
some evidence IDs appear in more than one challenge category.

Overlapping `fitting_manifest_v2.csv` train challenge rows by category:

| challenge_category | rows |
| --- | ---: |
| `label_boundary_correction_candidate` | 12 |
| `exudate_vs_mixed_boundary` | 11 |
| `mixed_vs_dr_boundary` | 8 |
| `mixed_vs_exudate_boundary` | 6 |
| `subtle_dr_missed_as_normal` | 1 |

Overlapping `fitting_manifest_v2.csv` train challenge rows by review action:

| review_action | rows |
| --- | ---: |
| `keep_label_model_wrong` | 26 |
| `relabel_to_predicted` | 12 |

## Interpretation

The dry-run is useful as a stress-test design artifact, but it should not be
canonicalized yet. A canonical challenge set should be independent of training
rows for the models it evaluates. Because Baseline 003 used
`fitting_manifest_v2.csv`, the current v2 train overlap would make a future
challenge result harder to interpret unless those rows are removed from the
challenge set or sequestered from future fitting.

The challenge categories are still well targeted: they emphasize persistent
exudate, mixed, and DR-pattern boundary problems, plus low-quality and
second-review cases. The issue is readiness hygiene, not the basic challenge
set concept.

## Recommended Next Step

Create a revised dry-run before canonicalizing `challenge_manifest_v1.csv`.
The revised dry-run should either:

- exclude rows whose evidence IDs are in `fitting_manifest_v2.csv` train, or
- define a future fitting/challenge split policy that explicitly sequesters
  challenge rows from training manifests.

After that revision, rerun this readiness audit and only then consider creating
canonical `challenge_manifest_v1.csv`.

## Safety

This audit is documentation-only.

- no training was performed
- no fitting execution was performed
- no model files were created
- no TFLite export was created
- no app/backend/runtime/model-loading files were changed
- no model promotion is approved
- no production claim is made
- `reviewed_manifest_v1.csv` remains unchanged
- `fitting_manifest_v1.csv` remains unchanged
- `fitting_manifest_v2.csv` remains unchanged
- canonical `challenge_manifest_v1.csv` remains absent
