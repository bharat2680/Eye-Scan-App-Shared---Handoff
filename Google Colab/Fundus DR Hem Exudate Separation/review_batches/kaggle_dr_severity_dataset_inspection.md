# Kaggle DR Severity Dataset Inspection

## Scope

Inspected the Kaggle competition page and small-file availability for:

- [Diabetic Retinopathy Detection | Kaggle](https://www.kaggle.com/competitions/diabetic-retinopathy-detection/data)

Goal:
- check whether this severity-labelled dataset is worth using to improve `dr_pattern_dominant` coverage
- avoid downloading the full image payload before approval

## What Was Checked

1. Kaggle competition page metadata and linked/manual-download references
2. publicly visible file references for the competition package
3. attempted access to the small label archive only: `trainLabels.csv.zip`

## Result of Small-File Access Attempt

A direct Kaggle CLI attempt to fetch only `trainLabels.csv.zip` returned `401 Unauthorized` with the currently configured local Kaggle token.

That means:
- no label archive was downloaded
- no image ZIPs were downloaded
- no existing datasets were modified

## Available Files Observed or Confirmed

From Kaggle-linked references and public mirrors, the competition package includes or references:

- `trainLabels.csv.zip`
- `train.zip`
- `test.zip`
- `sample.zip`
- `sampleSubmission.csv`

Notes:
- A public Academic Torrents mirror of the training package explicitly lists:
  - `sample.zip`
  - `train.zip`
  - `trainLabels.csv.zip`
- TensorFlow Datasets manual-download instructions for the Kaggle competition explicitly reference:
  - `test.zip`
  - `sample.zip`
  - `sampleSubmissions.csv`
  - `trainLabels.csv`

## trainLabels.csv Structure

The label CSV could not be fetched directly from Kaggle in this session, so the schema below is based on public code examples built for the official competition files.

Expected columns:

- `image`
- `level`

Interpretation:
- `image` is the base image identifier, for example `10_left` or `10_right`
- `level` is the DR severity label in the Kaggle five-class scale

## Number of Labelled Rows

Public references consistently report:

- `labelled rows = 35126`

## Severity Class Distribution

Public references consistently report the following `trainLabels.csv` class distribution:

- `0 = No DR = 25810`
- `1 = Mild = 2443`
- `2 = Moderate = 5292`
- `3 = Severe = 873`
- `4 = Proliferative DR = 708`

Useful aggregate for our lane:

- `levels 2-4 total = 6873`

That is a materially larger moderate/severe/proliferative pool than what we have been able to mine from the current generic DR folder.

## Left/Right Eye Pairing

This dataset appears to use left/right eye naming pairs.

Observed/expected pattern from public code examples:

- `10_left`
- `10_right`
- `13_left`
- `13_right`

So the filename stem likely encodes:
- patient/image ID prefix
- eye side suffix: `left` or `right`

## Can CSV Names Map to train.zip Members?

Yes, very likely.

Public code examples built on the Kaggle files map each CSV `image` value to an image file by appending `.jpeg`, for example:

- CSV name: `10_left`
- expected image member: `10_left.jpeg`

This strongly suggests the label CSV can be mapped directly to `train.zip` members once we choose to download or mount that ZIP.

## Comparison Against Current DR Folder

Current DR-folder review evidence:

- `37` accepted `dr_pattern_dominant` rows after `503` reviewed images

Interpretation:
- the current generic DR folder is noisy
- it yields many exudate-heavy, mixed, non-specific, or low-confidence rows
- it is not especially efficient for finding clean broader `dr_pattern_dominant` examples

Compared with that, the Kaggle severity-labelled dataset looks more promising because:

- it has explicit severity labels
- levels `2`, `3`, and `4` are likely enriched for broader disease burden
- we can bias screening toward moderate/severe/proliferative cases instead of random DR-folder slicing

## Recommendation

This dataset looks worth using for `dr_pattern_dominant` improvement, but only with a targeted screening strategy.

Recommended first step after approval:

1. Download only `trainLabels.csv.zip` if still needed locally, or otherwise obtain `trainLabels.csv`
2. Build a review-only candidate manifest from levels `2`, `3`, and `4`
3. Create a small contact-sheet screening batch, not a full export

Suggested first contact-sheet strategy:

- sample only a small targeted subset from levels `2-4`
- prefer `Moderate`, `Severe`, and `Proliferative DR`
- do **not** start by pulling all labelled images

Suggested first review batch size:

- `60-120` images total for screening

Suggested composition:

- `30-50` from level `2`
- `15-30` from level `3`
- `15-30` from level `4`

Reason:
- level `2` is large enough to provide meaningful variety
- levels `3` and `4` are smaller but more likely to contain broader global DR-pattern burden
- this should be a more efficient route to true `dr_pattern_dominant` candidates than additional random slicing from the current DR folder

## Safety Note

If we use this source later:
- Kaggle severity labels should remain `proposed_label` only
- ChatGPT visual review should still decide whether a case is truly `dr_pattern_dominant`
- no `reviewed_manifest_v1.csv`, `fitting_manifest_v1.csv`, or training should happen until after visual review

## Sources Used

- Kaggle competition page: [Diabetic Retinopathy Detection | Kaggle](https://www.kaggle.com/competitions/diabetic-retinopathy-detection/data)
- TensorFlow Datasets catalog/manual-download notes for this Kaggle competition
- Public training-package mirror listing file names and sizes
- Public code examples that read `trainLabels.csv` with columns `image` and `level` and map names to `.jpeg` images
