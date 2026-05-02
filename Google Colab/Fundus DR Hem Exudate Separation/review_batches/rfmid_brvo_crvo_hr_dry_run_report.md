# RFMiD BRVO/CRVO/HR Dry-Run Report

## Purpose

This is a dry-run only inspection for the weak future class
`hemorrhage_pattern_dominant_non_dr`.

The goal of this step was to check whether the locally available RFMiD labels
already provide plausible non-DR vascular/hemorrhage exploratory candidates,
and whether those candidate IDs can be matched to image filenames inside the
existing RFMiD image ZIP without extracting it.

No manifest was created in this step.
No ZIP extraction was performed.

## Inspected Paths

- `/Volumes/My Passport/Datasets/External Fundus/RFMiD Datasets/a. RFMiD_Training_Labels.csv`
- `/Volumes/My Passport/Datasets/External Fundus/RFMiD Datasets/b. RFMiD_Validation_Labels.csv`
- `/Volumes/My Passport/Datasets/External Fundus/RFMiD Datasets/c. RFMiD_Testing_Labels.csv`
- `/Volumes/My Passport/Datasets/External Fundus/1. Original Images.zip`

## Candidate Rule Used

A row was treated as an exploratory candidate if:

- `BRVO == 1`, or
- `CRVO == 1`, or
- `HR == 1`

These source labels are only useful as `proposed_label` seeds for future review.
They are not final labels.

## CSV Candidate Counts

### Per-split counts

| CSV | Rows | BRVO positives | CRVO positives | HR positives | Candidate rows |
| --- | ---: | ---: | ---: | ---: | ---: |
| `a. RFMiD_Training_Labels.csv` | 1920 | 73 | 28 | 0 | 101 |
| `b. RFMiD_Validation_Labels.csv` | 640 | 23 | 8 | 0 | 31 |
| `c. RFMiD_Testing_Labels.csv` | 640 | 23 | 9 | 1 | 33 |

### Aggregate counts

- Total `BRVO` candidate rows: `119`
- Total `CRVO` candidate rows: `45`
- Total `HR` candidate rows: `1`
- Total split-aware candidate rows (`train/val/test + ID`): `165`
- Deduplicated numeric `ID` count across all three CSVs: `156`

Note: RFMiD numeric IDs repeat across different splits, so the practical mapping
unit for image lookup is `split + ID`, not just `ID` alone.

## ZIP Filename Mapping Rule

Expected image paths inside `1. Original Images.zip` were mapped as:

- training row `ID = N` -> `1. Original Images/a. Training Set/N.png`
- validation row `ID = N` -> `1. Original Images/b. Validation Set/N.png`
- testing row `ID = N` -> `1. Original Images/c. Testing Set/N.png`

Example ZIP entries observed directly from listing:

- `1. Original Images/a. Training Set/1.png`
- `1. Original Images/a. Training Set/10.png`
- `1. Original Images/a. Training Set/100.png`
- `1. Original Images/a. Training Set/1000.png`
- `1. Original Images/a. Training Set/1010.png`

This confirms that RFMiD label `ID` values align with numeric PNG filenames in
the ZIP.

## ZIP Presence Check

- Missing image count for split-aware candidate rows: `0`
- Candidate rows with exact split-aware image match: `165 / 165`

So the RFMiD original image ZIP is sufficient for a future exploratory review
batch without requiring extraction in this inspection step.

## Example Candidate Rows

| CSV | ID | Positive label(s) | Disease_Risk | DR | Expected image path | Present in ZIP |
| --- | ---: | --- | ---: | ---: | --- | --- |
| `a. RFMiD_Training_Labels.csv` | 41 | `BRVO` | 1 | 0 | `1. Original Images/a. Training Set/41.png` | yes |
| `a. RFMiD_Training_Labels.csv` | 58 | `CRVO` | 1 | 0 | `1. Original Images/a. Training Set/58.png` | yes |
| `a. RFMiD_Training_Labels.csv` | 74 | `BRVO` | 1 | 0 | `1. Original Images/a. Training Set/74.png` | yes |
| `b. RFMiD_Validation_Labels.csv` | 88 | `BRVO` | 1 | 0 | `1. Original Images/b. Validation Set/88.png` | yes |
| `b. RFMiD_Validation_Labels.csv` | 117 | `BRVO` | 1 | 0 | `1. Original Images/b. Validation Set/117.png` | yes |
| `c. RFMiD_Testing_Labels.csv` | 2 | `BRVO` | 1 | 1 | `1. Original Images/c. Testing Set/2.png` | yes |
| `c. RFMiD_Testing_Labels.csv` | 25 | `HR` | 1 | 0 | `1. Original Images/c. Testing Set/25.png` | yes |
| `c. RFMiD_Testing_Labels.csv` | 93 | `CRVO` | 1 | 0 | `1. Original Images/c. Testing Set/93.png` | yes |

## Interpretation

This is a much stronger exploratory source than the earlier small local
hemorrhage folder.

Key strengths:

- `BRVO` and `CRVO` are explicitly present in RFMiD labels.
- Every split-aware candidate row matched an image path inside the existing RFMiD
  original image ZIP.
- The candidate pool is large enough for controlled review batching.

Important caution:

- `DR` is also positive for at least some vascular candidate rows, so the RFMiD
  disease labels should still be treated as `proposed_label` only.
- `HR` is extremely sparse in these RFMiD CSVs (`1` row total), so the more
  practical first source labels for this lane are `BRVO` and `CRVO`, with `HR`
  included opportunistically rather than as a standalone source bucket.

## Recommended Next Step

Create an RFMiD `BRVO` / `CRVO` / `HR` exploratory raw candidate manifest,
dry-run first, then create:

- `RFMiD BRVO/CRVO/HR review batch 001`
- matching contact sheet

Still no training at that step.

## Safety Note

RFMiD source disease labels are `proposed_label` only.
`final_label` must still come from visual review before any reviewed or fitting
manifest is considered.
