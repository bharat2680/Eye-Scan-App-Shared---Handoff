# Class Coverage Summary

## Scope

This document summarizes review evidence created so far for:

- `fundus_dr_hem_exudate_separation_v1`

This is **review evidence only**.

It is **not** a `reviewed_manifest_v1.csv`.
It is **not** a `fitting_manifest_v1.csv`.
It does **not** approve training.

All counts below come from the currently available ChatGPT visual review CSVs and
the previously documented planning/review notes already in the repository.

## Reviewed Artifacts

### 1. `normal_or_non_specific_review_batch_001_chatgpt_visual_reviewed.csv`

- File path:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/Google Colab/Fundus DR Hem Exudate Separation/review_batches/normal_or_non_specific_review_batch_001_chatgpt_visual_reviewed.csv`
- `row_count = 50`
- `accepted_rows = 50`
- `needs_second_review_rows = 0`
- Final-label counts:
  - `normal_or_non_specific = 50`
  - `dr_pattern_dominant = 0`
  - `exudate_macular_pattern_dominant = 0`
  - `mixed_hemorrhage_exudate_pattern = 0`
  - `hemorrhage_pattern_dominant_non_dr = 0`
- `train_val_test_rows = 0`
- `split_unset_rows = 50`
- `challenge_only_true = 0`

### 2. `dr_pattern_dominant_review_batch_001_chatgpt_visual_reviewed.csv`

- File path:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/Google Colab/Fundus DR Hem Exudate Separation/review_batches/dr_pattern_dominant_review_batch_001_chatgpt_visual_reviewed.csv`
- `row_count = 50`
- `accepted_rows = 31`
- `needs_second_review_rows = 19`
- Final-label counts:
  - `normal_or_non_specific = 4`
  - `dr_pattern_dominant = 0`
  - `exudate_macular_pattern_dominant = 17`
  - `mixed_hemorrhage_exudate_pattern = 10`
  - `hemorrhage_pattern_dominant_non_dr = 0`
- `train_val_test_rows = 0`
- `split_unset_rows = 50`
- `challenge_only_true = 0`

### 3. `dr_source_exudate_mixed_review_batch_002_chatgpt_visual_reviewed.csv`

- File path:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/Google Colab/Fundus DR Hem Exudate Separation/review_batches/dr_source_exudate_mixed_review_batch_002_chatgpt_visual_reviewed.csv`
- `row_count = 50`
- `accepted_rows = 32`
- `needs_second_review_rows = 18`
- Final-label counts:
  - `normal_or_non_specific = 3`
  - `dr_pattern_dominant = 0`
  - `exudate_macular_pattern_dominant = 14`
  - `mixed_hemorrhage_exudate_pattern = 8`
  - `hemorrhage_pattern_dominant_non_dr = 7`
- `train_val_test_rows = 0`
- `split_unset_rows = 50`
- `challenge_only_true = 0`

### 4. `hemorrhage_non_dr_review_batch_001_chatgpt_visual_reviewed.csv`

- File path:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/Google Colab/Fundus DR Hem Exudate Separation/review_batches/hemorrhage_non_dr_review_batch_001_chatgpt_visual_reviewed.csv`
- `row_count = 12`
- `accepted_rows = 8`
- `needs_second_review_rows = 4`
- Final-label counts:
  - `normal_or_non_specific = 6`
  - `dr_pattern_dominant = 0`
  - `exudate_macular_pattern_dominant = 0`
  - `mixed_hemorrhage_exudate_pattern = 0`
  - `hemorrhage_pattern_dominant_non_dr = 2`
- `train_val_test_rows = 0`
- `split_unset_rows = 12`
- `challenge_only_true = 0`

### 5. `rfmid_vascular_review_batch_001_chatgpt_visual_reviewed.csv`

- File path:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/Google Colab/Fundus DR Hem Exudate Separation/review_batches/rfmid_vascular_review_batch_001_chatgpt_visual_reviewed.csv`
- `row_count = 50`
- `accepted_rows = 35`
- `needs_second_review_rows = 15`
- Final-label counts:
  - `normal_or_non_specific = 1`
  - `dr_pattern_dominant = 0`
  - `exudate_macular_pattern_dominant = 4`
  - `mixed_hemorrhage_exudate_pattern = 13`
  - `hemorrhage_pattern_dominant_non_dr = 17`
- `train_val_test_rows = 0`
- `split_unset_rows = 50`
- `challenge_only_true = 0`

### 6. `rfmid_vascular_review_batch_002_chatgpt_visual_reviewed.csv`

- File path:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/Google Colab/Fundus DR Hem Exudate Separation/review_batches/rfmid_vascular_review_batch_002_chatgpt_visual_reviewed.csv`
- `row_count = 50`
- `accepted_rows = 36`
- `needs_second_review_rows = 14`
- Final-label counts:
  - `normal_or_non_specific = 2`
  - `dr_pattern_dominant = 0`
  - `exudate_macular_pattern_dominant = 3`
  - `mixed_hemorrhage_exudate_pattern = 14`
  - `hemorrhage_pattern_dominant_non_dr = 17`
- `train_val_test_rows = 0`
- `split_unset_rows = 50`
- `challenge_only_true = 0`

## Combined Totals Across Reviewed Artifacts

- `total rows reviewed = 262`
- `accepted rows = 192`
- `needs_second_review rows = 70`

Final-label totals:

- `normal_or_non_specific = 66`
- `dr_pattern_dominant = 0`
- `exudate_macular_pattern_dominant = 38`
- `mixed_hemorrhage_exudate_pattern = 45`
- `hemorrhage_pattern_dominant_non_dr = 43`

Split-state totals:

- `train_val_test_rows = 0`
- `split_unset_rows = 262`
- `challenge_only_true = 0`

## Interpretation

This is still review evidence only.
It is not a reviewed manifest and not a fitting manifest.
No training is approved from this summary.

### What improved

RFMiD materially improved `hemorrhage_pattern_dominant_non_dr` coverage.

Before the RFMiD vascular review batches, the exploratory hemorrhage source only
produced a very small number of accepted non-DR hemorrhage examples.

The two RFMiD vascular batches contributed:

- `hemorrhage_pattern_dominant_non_dr = 34`
- `mixed_hemorrhage_exudate_pattern = 27`
- `exudate_macular_pattern_dominant = 7`
- `normal_or_non_specific = 3`

That made the previously weakest class much more viable as a future review lane.

### What remains weak

The strongest remaining gap is `dr_pattern_dominant`.

Accepted reviewed evidence currently shows:

- `dr_pattern_dominant = 0`

That does not mean the class is invalid.
It means the current reviewed batches have mostly surfaced:

- exudate-dominant cases
- mixed hemorrhage/exudate cases
- hemorrhage-dominant vascular cases
- normal/non-specific cases

So the lane now has a better hemorrhage-vs-exudate-vs-mixed picture than it had
before, but still lacks accepted reviewed examples that clearly stay inside the
`dr_pattern_dominant` bucket.

## Recommendation

Recommended next step: **pause and inspect class balance first**, rather than
immediately starting RFMiD batch 003.

Reason:

- RFMiD has already materially strengthened the weak
  `hemorrhage_pattern_dominant_non_dr` class.
- The bigger imbalance now is not hemorrhage scarcity.
- The bigger issue is that accepted reviewed evidence for
  `dr_pattern_dominant` is still missing.

So before creating another RFMiD vascular batch, it would be safer to:

1. inspect the current accepted class balance,
2. decide whether another RFMiD vascular batch is still needed,
3. and likely open a new targeted DR-pattern sourcing/review pass to recover
   genuine `dr_pattern_dominant` examples.

If another RFMiD batch is created later, it should be because:

- we still want more hemorrhage-dominant vascular diversity, or
- we want more mixed vascular examples,

not because the current lane is short on non-DR hemorrhage evidence overall.

## Full-Image Review Warning

Full-image review is still recommended before creating any fitting manifest.

Current accepted labels were assigned from contact-sheet review assistance and
should not be promoted directly into training export without a more careful
image-level pass, especially for:

- subtle hemorrhage-vs-mixed calls,
- exudate-vs-mixed calls,
- vascular images with overlapping DR labels,
- low-confidence or haze-affected rows currently marked
  `needs_second_review`

## Safety Validation

- No `reviewed_manifest_v1.csv` was created.
- No `fitting_manifest_v1.csv` was created.
- No `challenge_manifest_v1.csv` was created.
- No train/val/test split was created.
- No training artifacts were created.
- No datasets were moved, copied, or deleted.
- RFMiD ZIP was not extracted.
- Preserved baselines remain untouched.
