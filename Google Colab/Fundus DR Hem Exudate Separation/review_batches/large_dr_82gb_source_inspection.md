# Large DR 82GB Source Inspection

## Scope

This is a source inspection note only for the EyeScan fundus DR evidence lane.
It does not add reviewed evidence, does not create fitting or challenge
manifests, and does not approve training.

## Archive Path

- User-provided Windows path:
  `F:\Datasets\DR-Diabetic Retinopathy\diabetic-retinopathy-detection.zip`
- Verified local macOS path:
  `/Volumes/My Passport/Datasets/DR-Diabetic Retinopathy/diabetic-retinopathy-detection.zip`
- Archive size: 88,310,951,633 bytes, about 88.31 GB / 82.25 GiB
- Sum of outer member uncompressed sizes: 88,289,103,740 bytes, about 82.23 GiB
- Outer ZIP entry count: 15

## Top-Level Structure

The outer archive is not a normal image-folder dataset. It is a wrapper around
small metadata ZIPs plus multi-part train/test ZIP chunks:

| Entry | Compressed bytes | Uncompressed bytes | Notes |
| --- | ---: | ---: | --- |
| `sample.zip` | 10,908,151 | 10,905,224 | Tiny sample image ZIP |
| `sampleSubmission.csv.zip` | 42,403 | 83,511 | Test submission CSV ZIP |
| `test.zip.001` through `test.zip.007` | 53,302,815,078 total | 53,289,598,430 total | Split test ZIP chunks |
| `train.zip.001` through `train.zip.005` | 34,997,127,084 total | 34,988,445,506 total | Split train ZIP chunks |
| `trainLabels.csv.zip` | 56,579 | 71,069 | Train label CSV ZIP |

All outer members use ZIP deflate compression. The train/test image archives are
split ZIP chunks inside the outer ZIP, so listing or extracting training images
requires reassembling or otherwise handling the split ZIP outside the repo.

## Label CSVs Found

### `trainLabels.csv.zip/trainLabels.csv`

- Columns: `image`, `level`
- Row count: 35,126
- Label type: severity-based numeric DR level
- Observed level counts:
  - `0` / `No_DR`: 25,810
  - `1` / `Mild`: 2,443
  - `2` / `Moderate`: 5,292
  - `3` / `Severe`: 873
  - `4` / `Proliferative_DR`: 708

The archive does not include a README with a text label map, but this matches
the standard Kaggle Diabetic Retinopathy Detection severity convention where
`0` is no DR and `1`-`4` are increasing DR severity.

### `sampleSubmission.csv.zip/sampleSubmission.csv`

- Columns: `image`, `level`
- Row count: 53,576
- All observed `level` values are `0`, which appears to be a placeholder
  submission value rather than reviewed labels.
- These test rows should not be treated as labelled evidence.

## Image Folder Structure

Direct train/test image folders are not visible at the outer ZIP level.

Observed sample ZIP structure:

- `sample/10_left.jpeg`
- `sample/10_right.jpeg`
- `sample/13_left.jpeg`
- `sample/13_right.jpeg`
- `sample/15_left.jpeg`
- `sample/15_right.jpeg`
- `sample/16_left.jpeg`
- `sample/16_right.jpeg`
- `sample/17_left.jpeg`
- `sample/17_right.jpeg`

Sample image dimensions inspected in memory:

- 2 images at `4752x3168`
- 2 images at `2592x1944`
- 2 images at `4928x3264`
- 4 images at `3888x2592`

This confirms the source is high-resolution/original-style JPEG data, not the
224x224 processed format used by the earlier Batch 008 Kaggle 224 source.

## Label-To-Image Mapping

The label rows use image IDs such as `10_left`, with expected image filenames
such as `10_left.jpeg`.

Partial safe mapping check:

- The 10 images in `sample.zip` all map to IDs in `trainLabels.csv`.
- Sample labels include levels `0`, `1`, `2`, and `4`.

Full label-to-train-image mapping was not verified in this inspection because
the train images are inside nested split ZIP chunks. Verifying all 35,126 train
image members would require reassembling or listing the split train ZIP outside
the repo, which was intentionally not done here.

## Relationship To The Older Kaggle 224 Source

This dataset appears to be a different, larger, higher-resolution Kaggle
Diabetic Retinopathy Detection source rather than the already inspected Kaggle
224x224 2019 source used for Batch 008.

Key differences:

- This archive has 35,126 labelled training rows, not 3,662 rows.
- Labels are numeric severity levels in `trainLabels.csv`, not class folders.
- Sample images are high-resolution JPEGs, not 224x224 images.
- Train/test images are packaged as large split ZIP chunks.

There may be conceptual label overlap because both are DR severity datasets, but
the packaging, row counts, and image resolution indicate this is not a direct
copy of the smaller 224x224 source.

## Preview Index Created

Created a tiny label-only preview index:

- `Google Colab/Fundus DR Hem Exudate Separation/review_batches/large_dr_82gb_source_preview/large_dr_82gb_preview_index.csv`

Preview index contents:

- 50 rows total
- 10 `No_DR`
- 10 `Mild`
- 10 `Moderate`
- 10 `Severe`
- 10 `Proliferative_DR`

No image files were copied into the repository. No contact sheets were created
because the full train image archive was not reassembled or extracted.

## Disk And Runtime Concerns

- The outer archive is about 82.25 GiB.
- The train split chunks alone represent about 32.59 GiB before extracting
  images.
- The test split chunks represent about 49.63 GiB before extracting images.
- Any future image-level inspection should use an external scratch location with
  ample free disk and must not copy a large dataset into the repository.
- Future work should first verify split-ZIP integrity and train label-to-image
  mapping before building any review pack.
- A local-only split-ZIP access plan has been added at
  `Google Colab/Fundus DR Hem Exudate Separation/review_batches/large_dr_82gb_source_preview/large_dr_82gb_split_zip_access_plan.md`.

## Usefulness Assessment

This source looks partially useful to likely useful for improving clean
DR-pattern evidence, but only after a careful review-first extraction lane:

- Useful signal: 6,873 labelled training rows are `Moderate`, `Severe`, or
  `Proliferative_DR`.
- Useful signal: sample images are high-resolution and likely better for lesion
  review than 224x224 thumbnails.
- Constraint: severity labels are source labels only; they are not accepted
  lesion-pattern labels.
- Constraint: `Moderate`, `Severe`, and `Proliferative_DR` do not guarantee
  clean `dr_pattern_dominant` evidence.
- Constraint: label-to-image mapping is only partially verified so far.

## Recommended Next Step

Do not create a full review pack yet.

If explicitly approved later, start a separate external-scratch verification
step that:

1. Reassembles or safely lists only the train split ZIP outside the repository.
2. Confirms all `trainLabels.csv` image IDs map to train JPEG members.
3. Extracts a very small review-only sample from `Moderate`, `Severe`, and
   `Proliferative_DR` rows only.
4. Creates contact sheets and an index for manual visual review before any
   reviewed-manifest proposal.

No rows should be added to `reviewed_manifest_v1.csv` from this source until
that future visual review lane is explicitly approved and completed.
