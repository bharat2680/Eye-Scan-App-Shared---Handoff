# Round 1 Proposed Corrections Package

This folder contains proposal-only outputs derived from the Baseline 001/002 Round 1 error-slice review-support package.

## Files

- `baseline_001_002_round1_proposed_corrections.csv`: rows marked `relabel_to_predicted` for proposed correction review.
- `baseline_001_002_round1_proposed_exclusions.csv`: rows marked `downgrade_needs_second_review` or `unusable_low_quality` for review-hold/exclusion handling.
- `baseline_001_002_round1_unassigned_review_hold.csv`: unassigned rows with no proposed action.
- `BASELINE_001_002_ROUND1_PROPOSED_CORRECTIONS_SUMMARY.md`: counts, interpretation, and guardrails.

## Rules

- Proposal-only; do not apply directly to canonical manifests.
- Do not modify `reviewed_manifest_v1.csv` or `fitting_manifest_v1.csv` from this package without a separate reviewed correction step.
- Do not create `challenge_manifest_v1.csv` from this package.
- Do not run Baseline 003 until the proposed corrections are reviewed.
- Do not promote or integrate any model from this package.
