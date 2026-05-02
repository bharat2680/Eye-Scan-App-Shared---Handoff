# Batch 008 Accepted DR-Pattern Proposed Addition Summary

This is a proposed evidence-addition file only.

It combines accepted clean DR-pattern candidates from Batch 008A and Batch 008B.
It does not modify `reviewed_manifest_v1.csv` yet unless explicitly approved.
It does not modify `fitting_manifest_v1.csv`.
It does not modify `challenge_manifest_v1.csv`.
It performs no training.
It performs no fitting.
It performs no model, app, backend, or runtime changes.
It performs no preserved-package changes.

The 98 rows should be reviewed as a final proposed addition before manifest
promotion.

## Counts

| Source | Accepted rows |
| --- | ---: |
| Batch 008A | 14 |
| Batch 008B | 84 |
| **Total** | **98** |

## Source Class Mix

| Source class | Rows |
| --- | ---: |
| `Moderate` | 87 |
| `Proliferate_DR` | 5 |
| `Severe` | 6 |

## Confidence Mix

| Confidence | Rows |
| --- | ---: |
| `low_medium` | 87 |
| `medium` | 11 |


## Proposed Action

Every row uses:

- `accepted_bucket = dr_pattern_dominant`
- `reviewer_decision = accepted_clean_dr_pattern_candidate`
- `proposed_action = propose_add_to_reviewed_manifest_only_after_final_approval`

No downgraded, second-review, unusable, mixed, exudate, or normal/non-specific
rows are included.
