# Round 1 Error-Slice Review Guide

## Purpose

This guide supports manual visual review of the Baseline 001/002 error-slice visual review pack. The goal is label-boundary analysis for the main unresolved confusion classes, not automatic relabeling.

Round 1 review must not modify `reviewed_manifest_v1.csv`, `fitting_manifest_v1.csv`, or create `challenge_manifest_v1.csv`. It must not trigger training, fitting execution, model export, TFLite export, app integration, or production claims.

## Source Pack

- Visual review index: `baseline_001_002_error_slice_visual_review_index.csv`
- Round 1 review template: `baseline_001_002_error_slice_round1_review_template.csv`
- Contact sheets: `contact_sheets/`
- Source rows: 197

Each row is a model error candidate from Baseline 001 and/or Baseline 002. The displayed true class is the current fitting evidence bucket, and the displayed predicted class is the model output for that run. Neither field is a clinical diagnosis.

## Allowed Review Actions

Use only one of these values in `review_action`:

- `keep_label_model_wrong`
- `relabel_to_predicted`
- `relabel_to_mixed`
- `downgrade_needs_second_review`
- `unusable_low_quality`
- `exclude_from_future_fitting`

Use `corrected_bucket` only when the reviewer believes a future correction proposal may be appropriate. Leave it blank when keeping the current label, when uncertain, or when marking the image unusable.

Use `confidence_low_medium_high` with one value: `low`, `medium`, or `high`.

## Decision Rules

### `dr_pattern_dominant` predicted as `normal_or_non_specific`

- Use `keep_label_model_wrong` if visible DR-pattern lesions exist, even if subtle.
- Use `downgrade_needs_second_review` if lesion evidence is too faint, low contrast, or uncertain.
- Use `relabel_to_predicted` only if no visible abnormality is present.

### `exudate_macular_pattern_dominant` predicted as `mixed_hemorrhage_exudate_pattern`

- Use `keep_label_model_wrong` if exudates dominate and hemorrhage evidence is weak or absent.
- Use `relabel_to_mixed` only if clear hemorrhage plus exudate is visible.
- Use `downgrade_needs_second_review` if image quality is low or the boundary is ambiguous.

### `mixed_hemorrhage_exudate_pattern` predicted as `dr_pattern_dominant`

- Use `keep_label_model_wrong` if both hemorrhage and exudate features are clearly visible.
- Use `relabel_to_predicted` if DR pattern dominates and exudate evidence is weak.
- Use `downgrade_needs_second_review` if mixed evidence is subtle or uncertain.

### `mixed_hemorrhage_exudate_pattern` predicted as `exudate_macular_pattern_dominant`

- Use `keep_label_model_wrong` if hemorrhage evidence is visible.
- Use `relabel_to_predicted` if exudate dominates and hemorrhage evidence is absent or very weak.
- Use `downgrade_needs_second_review` if the row is ambiguous.

## Review Notes

Prefer short, concrete notes about visible evidence, image quality, and uncertainty. Do not write diagnosis claims. If a row appears duplicated across Baseline 001 and Baseline 002, review the image evidence consistently but keep the rows separate because each row records a run-specific error.

Round 1 outputs are review notes only. Any future manifest change must be proposed and reviewed separately.
