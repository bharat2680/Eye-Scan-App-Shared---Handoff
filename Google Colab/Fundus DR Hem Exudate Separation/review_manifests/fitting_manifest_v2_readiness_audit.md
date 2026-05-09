# Fitting Manifest v2 Dry-Run Readiness Audit

## Scope

This audit reviews the balanced fitting manifest v2 dry run only. It does not create `fitting_manifest_v2.csv`, modify `reviewed_manifest_v1.csv`, modify canonical `fitting_manifest_v1.csv`, create `challenge_manifest_v1.csv`, run training, export a model, export TFLite, or change app/backend/runtime/model-loading files.

## Input Audited

- Dry-run candidate: `proposed_fitting_manifest_v2_balanced_dry_run/fitting_manifest_v2_balanced_dry_run.csv`
- Source correction dry run: `proposed_fitting_manifest_v1_round1_correction/fitting_manifest_v1_round1_correction_dry_run.csv`

The prompt referenced `proposed_fitting_manifest_v1_round1_correction/fitting_manifest_v2_balanced_dry_run.csv`, but the committed v2 balanced dry-run file is under `proposed_fitting_manifest_v2_balanced_dry_run/`.

## Count Verification

- Total v2 dry-run rows: 1,696
- Unique `evidence_id` values: 1,696
- Unique `image_path` values: 1,696
- `image_path` present for all rows: yes

### Class Counts

- `normal_or_non_specific`: 424
- `dr_pattern_dominant`: 424
- `exudate_macular_pattern_dominant`: 424
- `mixed_hemorrhage_exudate_pattern`: 424

### Split Counts

- `train`: 1,184
- `val`: 256
- `test`: 256

### Per-Class Split Counts

| Class | Train | Val | Test |
| --- | ---: | ---: | ---: |
| `normal_or_non_specific` | 296 | 64 | 64 |
| `dr_pattern_dominant` | 296 | 64 | 64 |
| `exudate_macular_pattern_dominant` | 296 | 64 | 64 |
| `mixed_hemorrhage_exudate_pattern` | 296 | 64 | 64 |

## Held-Out Row Check

The v2 dry run contains no rows with these Round 1 actions:

- `downgrade_needs_second_review`: 0
- `unusable_low_quality`: 0
- `unassigned`: 0

Included Round 1 action/status counts:

- Blank `round1_action`: 1,648
- `keep_label_model_wrong`: 26
- `relabel_to_predicted`: 22
- `unchanged_no_round1_action`: 1,648
- `unchanged_round1_keep_label_model_wrong`: 26
- `corrected_round1_relabel_to_predicted_dry_run`: 22

## Canonical Manifest Guardrails

- Canonical `fitting_manifest_v1.csv`: 1,864 rows
- `reviewed_manifest_v1.csv`: 2,955 rows
- `challenge_manifest_v1.csv`: absent

No canonical manifest files were changed by this audit.

## Readiness Assessment

The v2 dry run is cleaner than v1 because ambiguous/error-slice rows were held out and selected correction candidates were applied in the dry-run lineage. It is smaller than fitting v1 but more label-consistent for a future Baseline 003 lane.

The dry run is balanced at 424 rows per class and keeps equal per-class train/val/test splits. This makes it a strong candidate basis for a future canonical `fitting_manifest_v2.csv`, but it is not itself canonical yet.

## Recommendation

Create canonical `fitting_manifest_v2.csv` only after a separate approval step that verifies image path resolution for every row. Baseline 003 should only be considered after canonical `fitting_manifest_v2.csv` exists and image resolution is confirmed. No app/backend/model promotion is allowed from this audit.

## Git Diff Summary

Expected diff for this task: this audit markdown only.
