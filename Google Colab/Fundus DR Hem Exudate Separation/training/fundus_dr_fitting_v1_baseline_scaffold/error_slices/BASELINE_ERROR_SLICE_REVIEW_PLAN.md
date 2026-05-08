# Baseline Error-Slice Review Plan

This is a documentation-only scaffold for reviewing the unresolved Fundus DR
fitting v1 error slices from Baseline 001 and Baseline 002.

The purpose is label-boundary and error analysis. This plan does not relabel
rows, change manifests, run fitting/training, promote a model, export TFLite, or
approve app/backend/runtime integration.

## Source Runs

- Baseline 001:
  `Google Colab/Fundus DR Hem Exudate Separation/training/fundus_dr_fitting_v1_baseline_scaffold/runs/baseline_001/`
- Baseline 002:
  `Google Colab/Fundus DR Hem Exudate Separation/training/fundus_dr_fitting_v1_baseline_scaffold/runs/baseline_002/`

Current comparison conclusion:

- Baseline 001 remains the reference baseline.
- Baseline 002 did not materially improve held-out test macro F1.
- The main unresolved issue is confusion between exudate, mixed, and DR-pattern
  evidence classes.

## Per-Row Prediction Availability

Per-row prediction CSVs were not available in the committed run artifacts or in
the external Baseline 001/002 run folders checked on Dell/Windows.

Available artifacts are aggregate-only:

- training history CSV/JSON
- validation metrics JSON
- test metrics JSON
- classification report CSV/JSON
- confusion matrix CSV
- run log and run metadata
- external evaluation-only checkpoints

Because per-row predictions were not saved, this pass cannot identify actual
`evidence_id` values for the misclassified rows. The index CSV is therefore a
header-only scaffold until a future run or audit emits per-row predictions.

Future fitting runs should save a per-row prediction CSV for `val` and `test`
with at least:

- `run_name`
- `evidence_id`
- `true_class`
- `predicted_class`
- `split`
- `image_path`
- `resolved_external_path`
- `source_batch`
- `source_dataset`
- per-class probabilities or prediction confidence

## Target Error Slices

The review should focus on these held-out test-split error slices:

- `exudate_macular_pattern_dominant -> mixed_hemorrhage_exudate_pattern`
- `mixed_hemorrhage_exudate_pattern -> dr_pattern_dominant`
- `mixed_hemorrhage_exudate_pattern -> exudate_macular_pattern_dominant`
- `dr_pattern_dominant -> normal_or_non_specific`

Aggregate test confusion counts from the existing runs:

| error slice | Baseline 001 count | Baseline 002 count |
| --- | ---: | ---: |
| `exudate_macular_pattern_dominant -> mixed_hemorrhage_exudate_pattern` | 20 | 19 |
| `mixed_hemorrhage_exudate_pattern -> dr_pattern_dominant` | 18 | 22 |
| `mixed_hemorrhage_exudate_pattern -> exudate_macular_pattern_dominant` | 7 | 7 |
| `dr_pattern_dominant -> normal_or_non_specific` | 7 | 5 |

These counts confirm the error family, but they are not enough to select
individual rows for visual review.

## Review Index

The review index scaffold is:

- `baseline_001_002_error_slice_index.csv`

Expected columns:

- `run_name`
- `evidence_id`
- `true_class`
- `predicted_class`
- `split`
- `image_path`
- `source_batch`
- `source_dataset`
- `confidence_if_available`
- `error_slice`
- `review_action`
- `notes`

`review_action` and `notes` must remain blank until manual visual review.

Allowed future review actions:

- `keep_label`
- `relabel_to_predicted`
- `relabel_to_mixed`
- `downgrade_needs_second_review`
- `unusable_low_quality`
- `exclude_from_future_fitting`

## Manual Review Workflow

1. Produce or recover per-row prediction CSVs for Baseline 001 and Baseline 002.
2. Filter to the target error slices listed above.
3. Build a visual review pack for those rows only.
4. Review each image against its evidence-label boundary, not as a clinical
   diagnosis.
5. Record review decisions in the error-slice index or a derivative review
   table.
6. Do not update `reviewed_manifest_v1.csv` or `fitting_manifest_v1.csv`
   automatically.
7. Use the completed error-slice review to decide whether a Baseline 003 data
   lane is justified.

## Safety Statement

- no automatic relabeling
- no manifest changes
- no fitting or training changes
- no app/backend/runtime/model-loading changes
- no model promotion
- no production claim
- `challenge_manifest_v1.csv` remains absent

The next safe step before Baseline 003 is visual review of the target error
slices, backed by per-row prediction artifacts.
