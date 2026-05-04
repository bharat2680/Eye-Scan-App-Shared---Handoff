# Large DR Batch 001 ChatGPT Full Review Findings

Scope: full source-level Moderate review pack from the large/original Kaggle DR detection source.

Important: this is conservative AI-assisted contact-sheet triage for EyeScan evidence curation. It is not clinical diagnosis, not accepted evidence by itself, and not training data. The accepted rows are candidate-only until Codex integrates the handoff and Bharat explicitly approves any proposed manifest addition.

## Input pack

- Source review pack: `large_dr_batch_001_moderate_full_review_for_chatgpt.zip`
- Input rows reviewed: 5,292
- Source label for all rows: level 2 / Moderate
- Contact sheets reviewed: 331

## Manual bucket counts

| Manual bucket | Count |
|---|---:|
| `accept_dr_pattern_dominant` | 834 |
| `downgrade_exudate_macular` | 1080 |
| `downgrade_mixed_hemorrhage_exudate` | 466 |
| `downgrade_hemorrhage_non_dr` | 5 |
| `normal_or_non_specific` | 472 |
| `needs_second_review` | 1968 |
| `unusable_low_quality` | 467 |


## Accepted candidate interpretation

- Accepted clean DR-pattern candidates: 834
- These are candidate accepted rows only.
- They should be integrated as review-support first.
- Do not append them directly to `reviewed_manifest_v1.csv` without a separate proposed evidence-addition step.

## Safety boundary

- No training.
- No fitting.
- No app/backend/runtime/model changes.
- No preserved package changes.
- No `reviewed_manifest_v1.csv` change by this handoff.
- No `fitting_manifest_v1.csv` or `challenge_manifest_v1.csv` creation.
