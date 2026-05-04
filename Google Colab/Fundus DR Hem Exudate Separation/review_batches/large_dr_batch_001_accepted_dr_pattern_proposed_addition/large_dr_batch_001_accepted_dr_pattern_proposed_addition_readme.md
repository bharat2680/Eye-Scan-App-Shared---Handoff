# Large DR Batch 001 Accepted DR-Pattern Proposed Addition

## Purpose

This folder contains a proposed evidence-addition file only.

It combines only the 834 accepted clean DR-pattern candidates from Large DR
Batch 001. These candidates came from conservative ChatGPT contact-sheet review
findings for the source-level `Moderate` rows in the large/original Kaggle
Diabetic Retinopathy Detection train source.

## Files

- `large_dr_batch_001_accepted_dr_pattern_proposed_addition.csv`
- `large_dr_batch_001_accepted_dr_pattern_proposed_addition_summary.md`
- `large_dr_batch_001_accepted_dr_pattern_proposed_addition_readme.md`

## Important Interpretation

- This is not manifest promotion.
- These rows are not final clinical labels.
- Source severity label `Moderate` is not used as final truth.
- Accepted rows are proposed clean DR-pattern evidence candidates only.
- Rows should be reviewed as a final proposed addition before any
  `reviewed_manifest_v1.csv` promotion.

## Safety Boundary

- `reviewed_manifest_v1.csv` was not modified.
- `fitting_manifest_v1.csv` was not created.
- `challenge_manifest_v1.csv` was not created.
- No training was performed.
- No fitting was performed.
- No model, app, backend, runtime, or preserved-package files were changed.

## Proposed Action

Every row uses:

- `accepted_bucket = dr_pattern_dominant`
- `reviewer_decision = accepted_clean_dr_pattern_candidate`
- `proposed_action = propose_add_to_reviewed_manifest_only_after_final_approval`

No downgraded, second-review, normal/non-specific, exudate, mixed,
hemorrhage-non-DR, or unusable rows are included.
