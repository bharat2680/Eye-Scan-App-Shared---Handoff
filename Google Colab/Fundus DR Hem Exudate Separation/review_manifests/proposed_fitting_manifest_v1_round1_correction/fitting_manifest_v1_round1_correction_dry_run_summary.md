# Fitting Manifest v1 Round 1 Correction Dry Run

## Warning

This is a dry-run manifest only. It does not modify `reviewed_manifest_v1.csv`, the canonical `fitting_manifest_v1.csv`, or create `challenge_manifest_v1.csv`.
No training, fitting execution, model export, TFLite export, app/backend/runtime integration, or model promotion was performed.

## Inputs

- Canonical fitting manifest: `../fitting_manifest_v1.csv`
- Round 1 combined review support: `../../training/fundus_dr_fitting_v1_baseline_scaffold/error_slices/visual_review_pack/baseline_001_002_error_slice_round1_combined_review_support.csv`

## Proposal Row Counts

- Original `fitting_manifest_v1.csv` row count: 1864
- Total Round 1 review-support rows: 197
- Correction proposal rows (`relabel_to_predicted`): 50
- Needs-second-review rows removed/held (`downgrade_needs_second_review`): 81
- Unusable-low-quality rows removed/held (`unusable_low_quality`): 9
- Unassigned rows removed/held: 1
- Keep-label/model-wrong rows unchanged: 56

## Unique Canonical Fitting Row Effects

Round 1 review rows can repeat the same `evidence_id` across Baseline 001 and Baseline 002. The dry run applies changes once per canonical fitting row using conservative precedence: hold/exclusion/unassigned beats relabel, relabel beats keep-label.

- Unique affected fitting rows: 108
- Unique rows relabeled in dry run: 26
- Unique rows removed/held out in dry run: 55
- Unique keep-label rows left unchanged: 27
- Unaffected fitting rows left unchanged: 1756
- Evidence IDs with multiple Round 1 actions across baseline runs: 20

## Dry-Run Result

- New dry-run row count: 1809

## Class Counts After Corrections/Removals

- `dr_pattern_dominant`: 477
- `exudate_macular_pattern_dominant`: 442
- `mixed_hemorrhage_exudate_pattern`: 424
- `normal_or_non_specific`: 466

## Split Counts After Corrections/Removals

- `test`: 252
- `train`: 1304
- `val`: 253

## Balance Assessment

- Classes are imbalanced after the natural dry-run corrections/removals: yes
- Class count range after dry run: 53

## Recommendation

Create a future `fitting_manifest_v2_dry_run` that explicitly reviews these proposed corrections and rebalances classes/splits before Baseline 003. Do not run Baseline 003 from this natural dry-run manifest as-is.

## Guardrails

- `reviewed_manifest_v1.csv` remains unchanged.
- Canonical `fitting_manifest_v1.csv` remains unchanged.
- `challenge_manifest_v1.csv` remains absent.
- No training/model/app/backend/runtime changes were made.

## Git Diff Summary

Expected diff for this task: two new dry-run artifacts only:

- `fitting_manifest_v1_round1_correction_dry_run.csv`
- `fitting_manifest_v1_round1_correction_dry_run_summary.md`
