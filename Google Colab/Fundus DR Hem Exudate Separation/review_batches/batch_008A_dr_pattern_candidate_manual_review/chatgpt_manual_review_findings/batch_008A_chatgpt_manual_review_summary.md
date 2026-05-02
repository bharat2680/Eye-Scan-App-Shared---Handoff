# Batch 008A ChatGPT manual review findings

Scope: visual review of the 160 Batch 008A candidate images using the uploaded 4x4 contact sheets and index.

Boundary: this is EyeScan evidence curation support, not clinical diagnosis. The findings should not be used for direct training or manifest promotion without a Codex-controlled manifest lane and any additional review Bharat requests.

## Bucket counts

- `downgrade_mixed_hemorrhage_exudate`: 44
- `needs_second_review`: 36
- `downgrade_exudate_macular`: 31
- `normal_or_non_specific`: 20
- `accept_dr_pattern_dominant`: 14
- `downgrade_hemorrhage_non_dr`: 10
- `unusable_low_quality`: 5

## Counts by source class

### Moderate
- `downgrade_exudate_macular`: 16
- `normal_or_non_specific`: 13
- `downgrade_mixed_hemorrhage_exudate`: 12
- `needs_second_review`: 11
- `accept_dr_pattern_dominant`: 3

### Proliferate_DR
- `needs_second_review`: 24
- `downgrade_mixed_hemorrhage_exudate`: 16
- `downgrade_hemorrhage_non_dr`: 9
- `downgrade_exudate_macular`: 7
- `normal_or_non_specific`: 5
- `accept_dr_pattern_dominant`: 5
- `unusable_low_quality`: 5

### Severe
- `downgrade_mixed_hemorrhage_exudate`: 16
- `downgrade_exudate_macular`: 8
- `accept_dr_pattern_dominant`: 6
- `normal_or_non_specific`: 2
- `needs_second_review`: 1
- `downgrade_hemorrhage_non_dr`: 1

## Interpretation

Only rows marked `accept_dr_pattern_dominant` should be considered candidate clean DR-pattern anchors. Most selected rows were downgraded because exudates, macular clustering, large hemorrhage/proliferative features, laser/scar-like patterns, low quality, or nonspecific appearance made them unsuitable as clean DR anchors.

Recommended next step: ask Codex to integrate this findings CSV as review-support only, then prepare a proposed accepted-evidence manifest patch containing only `accept_dr_pattern_dominant` rows for Bharat review. Do not modify reviewed/fitting/challenge manifests yet.
