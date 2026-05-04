# Large DR Batch 001 ChatGPT Findings Integration Note

## Scope

This folder integrates the ChatGPT full-review findings handoff for Large DR
Batch 001 as review-support material only.

Batch 001 reviewed all 5,292 source-level `Moderate` rows from the
large/original Kaggle Diabetic Retinopathy Detection source contact-sheet pack.

## Files Integrated

- `large_dr_batch_001_chatgpt_full_review_findings.csv`
- `large_dr_batch_001_accept_dr_pattern_candidates_only.csv`
- `large_dr_batch_001_needs_second_review_only.csv`
- `large_dr_batch_001_chatgpt_full_review_summary.md`

## Interpretation

- These are conservative ChatGPT contact-sheet review findings.
- They are review-support findings only.
- They are not clinical diagnoses.
- They are not training labels.
- Accepted rows are candidate accepted rows only.
- Source severity labels remain source labels only.
- No rows are promoted to canonical reviewed evidence by this handoff.

## Verified Counts

- Full findings rows: 5,292
- Accepted clean DR-pattern candidate rows: 834
- Needs-second-review rows: 1,968

Manual bucket counts:

- `accept_dr_pattern_dominant`: 834
- `downgrade_exudate_macular`: 1,080
- `downgrade_mixed_hemorrhage_exudate`: 466
- `downgrade_hemorrhage_non_dr`: 5
- `normal_or_non_specific`: 472
- `needs_second_review`: 1,968
- `unusable_low_quality`: 467

## Safety Boundary

- `reviewed_manifest_v1.csv` was not modified.
- `fitting_manifest_v1.csv` was not created.
- `challenge_manifest_v1.csv` was not created.
- No training was performed.
- No fitting was performed.
- No model, app, backend, runtime, or preserved-package files were changed.

Any future evidence addition from these candidates must be a separate proposed
manifest-addition step and must be explicitly approved before
`reviewed_manifest_v1.csv` is changed.
