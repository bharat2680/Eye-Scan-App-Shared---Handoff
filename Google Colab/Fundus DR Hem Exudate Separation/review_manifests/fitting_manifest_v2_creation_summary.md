# Fitting Manifest v2 Creation Summary

## Source

- Created `fitting_manifest_v2.csv` from the approved Round 1 corrected balanced dry-run.
- Source used: `proposed_fitting_manifest_v2_balanced_dry_run/fitting_manifest_v2_balanced_dry_run.csv`
- Prompt-referenced source path `proposed_fitting_manifest_v1_round1_correction/fitting_manifest_v2_balanced_dry_run.csv` was not present in this checkout; the committed v2 dry-run path audited in `fitting_manifest_v2_readiness_audit.md` was used.

## Guardrails

- `fitting_manifest_v1.csv` remains preserved and unchanged.
- `reviewed_manifest_v1.csv` remains unchanged.
- `challenge_manifest_v1.csv` remains absent.
- No training was performed.
- No model files, TFLite exports, app/backend/runtime, or model-loading changes were made.
- No model was promoted.

## Intended Use

`fitting_manifest_v2.csv` is intended for a future Baseline 003 evaluation-only run after image path resolution is verified for every row.

## Count Verification

- Total rows: 1696
- Unique `evidence_id` values: 1696
- Unique `image_path` values: 1696

### Class Counts

- `normal_or_non_specific`: 424
- `dr_pattern_dominant`: 424
- `exudate_macular_pattern_dominant`: 424
- `mixed_hemorrhage_exudate_pattern`: 424

### Split Counts

- `train`: 1184
- `val`: 256
- `test`: 256

### Per-Class Split Counts

| Class | Train | Val | Test |
| --- | ---: | ---: | ---: |
| `normal_or_non_specific` | 296 | 64 | 64 |
| `dr_pattern_dominant` | 296 | 64 | 64 |
| `exudate_macular_pattern_dominant` | 296 | 64 | 64 |
| `mixed_hemorrhage_exudate_pattern` | 296 | 64 | 64 |

## Git Diff Summary

Expected diff for this task: `fitting_manifest_v2.csv` and this creation summary only.