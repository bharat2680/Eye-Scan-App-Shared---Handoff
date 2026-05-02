# Batch 008B ChatGPT Manual Review Findings Integration Note

This folder contains the Batch 008B ChatGPT remaining-candidate review findings.

These are conservative review-support findings only. They are not accepted
evidence labels, clinical diagnoses, training labels, or manifest updates.

Batch 008B covers the remaining `dr_pattern_dominant` candidates that were not
included in Batch 008A:

- rows reviewed: 175
- source class: `Moderate`
- contact sheets: 11
- accepted clean DR-pattern candidates: 84

Manual bucket counts:

| Manual bucket | Count |
| --- | ---: |
| `accept_dr_pattern_dominant` | 84 |
| `unusable_low_quality` | 65 |
| `downgrade_mixed_hemorrhage_exudate` | 14 |
| `needs_second_review` | 12 |

No rows are automatically promoted into `reviewed_manifest_v1.csv`.

No fitting, training, app/backend/runtime/model change, preserved-package change,
or integration lane is approved by this handoff.

If explicitly approved later, the safe next step is a separate proposed
evidence-addition patch that considers only accepted candidate rows.
