# Batch 008A DR-Pattern Candidate Manual Review Pack

## Purpose

Batch 008A is a manual review pack only.

It was derived from ChatGPT candidate triage for Batch 008 by selecting the top
`dr_pattern_dominant` candidates from `batch_008_chatgpt_candidate_findings.csv`.

Candidate labels are not accepted labels. They are review-support hints only.
Rows can only become accepted evidence after manual review.

The `chatgpt_manual_review_findings/` files are review-support findings only.
The 14 `accept_dr_pattern_dominant` rows are clean candidate rows for a future
proposed evidence-addition patch, not automatically accepted manifest rows.

## Selection

Selection rule:

1. filter to `chatgpt_candidate_review_bucket = dr_pattern_dominant`
2. sort by `candidate_confidence` descending
3. sort by `auto_quality_score` descending
4. select the top 160 candidates, or all candidates if fewer than 160 exist

Source `dr_pattern_dominant` candidate count: `335`

Selected row count: `160`

Contact-sheet count: `10`

Selected rows by source class:

| Source class | Selected rows |
| --- | ---: |
| `Moderate` | 55 |
| `Proliferate_DR` | 71 |
| `Severe` | 34 |

## Files

- `batch_008A_index.csv`: manual review index for the selected rows
- `batch_008A_contact_sheets/`: 4x4 contact sheets, maximum 16 images per sheet
- `chatgpt_manual_review_findings/`: ChatGPT conservative manual-review
  findings handoff, accepted-candidates-only CSV, summary, prompt handoff, and
  integration note
- `batch_008A_readme.md`: this note

The contact sheets show:

- `row_id`
- `source_class`
- `id_code`
- candidate bucket
- confidence
- `auto_quality_score`

## Manual Review Fields

The following fields are intentionally blank in `batch_008A_index.csv`:

- `manual_bucket`
- `reviewer_decision`
- `notes`

Allowed manual buckets:

- `accept_dr_pattern_dominant`
- `downgrade_mixed_hemorrhage_exudate`
- `downgrade_exudate_macular`
- `downgrade_hemorrhage_non_dr`
- `normal_or_non_specific`
- `needs_second_review`
- `unusable_low_quality`

## Safety Notes

- No rows were added to `reviewed_manifest_v1.csv`.
- No rows were added to `fitting_manifest_v1.csv`.
- No rows were added to `challenge_manifest_v1.csv`.
- No training was performed.
- No fitting was performed.
- No model changes were made.
- No app, backend, runtime, or model-loading changes were made.
- No preserved package changes were made.
- No automatic promotion to accepted evidence was performed.
