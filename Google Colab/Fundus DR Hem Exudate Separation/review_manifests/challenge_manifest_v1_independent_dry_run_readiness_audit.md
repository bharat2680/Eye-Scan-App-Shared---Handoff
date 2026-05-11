# Challenge Manifest v1 Independent Dry-Run Readiness Audit

This audit reviews
`proposed_challenge_manifest_v1/challenge_manifest_v1_dry_run_independent.csv`
as a fully independent evaluation stress-test candidate. It does not create
canonical `challenge_manifest_v1.csv`.

## Readiness Recommendation

The independent dry-run is eligible for canonical `challenge_manifest_v1.csv`
review from a fitting-manifest independence perspective.

It has zero evidence-ID overlap with `fitting_manifest_v2.csv`, no duplicate
challenge IDs, and no duplicate `evidence_id + challenge_category` pairs.
Before creating the canonical manifest, review whether 73 rows gives enough
coverage for the intended stress-test slices, especially because the set is now
heavily weighted toward `needs_second_review_boundary`.

## Count Verification

| check | result |
| --- | ---: |
| independent dry-run rows | 73 |
| duplicate `challenge_id` values | 0 |
| duplicate `evidence_id + challenge_category` pairs | 0 |
| `fitting_manifest_v2.csv` evidence-ID overlap | 0 |
| canonical `challenge_manifest_v1.csv` exists | no |
| `reviewed_manifest_v1.csv` rows | 2955 |
| `fitting_manifest_v1.csv` rows | 1864 |
| `fitting_manifest_v2.csv` rows | 1696 |

## Challenge Category Counts

| challenge_category | rows |
| --- | ---: |
| `needs_second_review_boundary` | 50 |
| `label_boundary_correction_candidate` | 13 |
| `low_quality_or_low_contrast` | 6 |
| `mixed_vs_dr_boundary` | 1 |
| `mixed_vs_exudate_boundary` | 1 |
| `model_disagreement` | 1 |
| `subtle_dr_missed_as_normal` | 1 |

The independent dry-run is smaller but cleaner than the original 128-row
dry-run because every row overlapping `fitting_manifest_v2.csv` was removed.
That independence makes it safer as a challenge candidate, but it also narrows
coverage of some boundary categories.

## Review Action Counts

| review_action | rows |
| --- | ---: |
| `downgrade_needs_second_review` | 50 |
| `relabel_to_predicted` | 13 |
| `unusable_low_quality` | 6 |
| `keep_label_model_wrong` | 3 |
| `unassigned` | 1 |

The set is heavily weighted toward rows requiring second review. Those rows are
useful for stress-testing uncertainty and boundary handling, but they must not
be treated as accepted disease truth.

## Expected Handling Counts

| expected_handling | rows |
| --- | ---: |
| `flag_for_second_review_not_training` | 50 |
| `label_boundary_candidate_requires_review` | 13 |
| `quality_stress_case_not_disease_truth` | 6 |
| `model_should_match_original_review_bucket` | 3 |
| `review_hold_before_canonical_use` | 1 |

Low-quality rows are quality stress cases only. They are not accepted disease
labels and should be evaluated as quality/exclusion behavior.

## Interpretation

This dry-run is a fully independent evaluation stress-test candidate relative
to `fitting_manifest_v2.csv`. It is smaller than the earlier dry-runs:

- original dry-run: 128 rows
- no-train-overlap dry-run: 90 rows
- independent dry-run: 73 rows

The reduction improves evaluation hygiene by removing all v2 overlap, but it
also makes the category distribution uneven. The independent set mostly tests
second-review boundary behavior, with a smaller number of label-boundary,
low-quality, and persistent model-error cases.

## Recommended Next Step

Review the independent dry-run before canonicalization. If 73 rows is enough
for the first challenge set, canonical `challenge_manifest_v1.csv` can be
created from this independent dry-run in a separate task. If broader category
coverage is needed, add future manually reviewed difficult cases that are not
present in fitting manifests.

Any canonical challenge manifest must stay separate from training and fitting
manifests.

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
