# Review Batches

These files are manual review batches only for
`fundus_dr_hem_exudate_separation_v1`.

They are not training-ready.

## Purpose

Batch files provide smaller, practical slices of the raw candidate manifest for
manual image review.

The current DR-pattern review batch was selected from:

- `Google Colab/Fundus DR Hem Exudate Separation/review_manifests/raw_candidate_manifest.csv`

## Rules

- `final_label` must remain empty until image review is completed.
- `proposed_label` is only a hint.
- `review_status` remains `unreviewed` until a reviewer changes it.
- `split` remains `unset` until rows are accepted and later assigned into a
  fitting plan.
- `challenge_only` remains `false` for these batch rows unless a reviewer later
  deliberately moves a row into a held-out challenge set.

## Fitting Safety

- Batch rows must not enter fitting until they are reviewed and accepted.
- Batch rows must not enter fitting while `final_label` is empty.
- Batch rows must not enter fitting while `split` is `unset`.
- These files do not create `reviewed_manifest_v1.csv`,
  `fitting_manifest_v1.csv`, or `challenge_manifest_v1.csv`.

## Current Batch

- `dr_pattern_dominant_review_batch_001.csv`
- `dr_pattern_dominant_review_batch_001_review_gallery.html`

This batch uses the raw DR candidate source manifest and keeps
`proposed_label = dr_pattern_dominant` on every row as a review hint only.

## Local Review Gallery

Open
`Google Colab/Fundus DR Hem Exudate Separation/review_batches/dr_pattern_dominant_review_batch_001_review_gallery.html`
locally in a browser.

The gallery is a manual review aid only:

- It references the same 50 image paths from the batch CSV.
- It does not write back to the CSV.
- It does not assign `final_label` automatically.
- It does not mark rows `accepted` automatically.
- Any `final_label`, `review_status`, or notes entered in the page are for
  human review assistance only and must be copied into a reviewed manifest
  later through an explicit review workflow.
