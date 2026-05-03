# Large DR 82GB Split-ZIP Access Plan

## Scope

This is a local-only access plan for future inspection of the large Kaggle
Diabetic Retinopathy Detection training images. It is documentation only.

No split ZIP files were reassembled while creating this plan. No training images
were extracted. No large image data was copied into the repository.

## Current External Source Path

- `/Volumes/My Passport/Datasets/DR-Diabetic Retinopathy/diabetic-retinopathy-detection.zip`

This path corresponds to the user-provided Windows source path:

- `F:\Datasets\DR-Diabetic Retinopathy\diabetic-retinopathy-detection.zip`

## Observed Internal Split Files

The outer archive contains split train and test ZIP members:

- `train.zip.001`
- `train.zip.002`
- `train.zip.003`
- `train.zip.004`
- `train.zip.005`
- `test.zip.001`
- `test.zip.002`
- `test.zip.003`
- `test.zip.004`
- `test.zip.005`
- `test.zip.006`
- `test.zip.007`

The train labels are stored separately in:

- `trainLabels.csv.zip`

The sample and submission helper files are:

- `sample.zip`
- `sampleSubmission.csv.zip`

## Why Full Extraction Into The Repo Is Forbidden

The repository should contain review metadata, tiny preview indexes, and small
review-support artifacts only. Full extraction into the repo is forbidden
because:

- the source archive is about 82.25 GiB;
- reassembled train/test ZIPs require tens of GiB;
- extracted JPEGs would require substantial additional space;
- raw dataset files would bloat Git history and make normal repository work
  impractical;
- source severity labels are not accepted lesion-pattern labels;
- no fitting, challenge, or training lane has been approved.

## Recommended Local-Only Working Location

Use an external scratch/work folder outside the repository, for example:

- `/Users/bharatsharma/Documents/EyeScan_Local_Data/large_dr_82gb_work/`

Suggested subfolders:

- `outer_members/`
- `reassembled/`
- `train_listings/`
- `tiny_preview_extract/`

Do not place these folders under
`/Users/bharatsharma/Documents/Playground/EyeScan_Shared/`.

## Disk-Space Estimate

- Source archive: about 82.25 GiB.
- Reassembled train ZIP: likely about 32.6 GiB.
- Extracted train images: significant additional space beyond the reassembled
  ZIP.
- Temporary copy of split parts plus reassembled train ZIP can require more
  than 65 GiB before any image extraction.
- Recommended free space before any full operation: at least 200-250 GiB.

If free space is below that range, do not run the full workflow. Prefer a
smaller targeted extraction path from verified split-ZIP tooling.

## Safe Staged Approach

### Stage A - Reassemble/List Train Split ZIP Outside The Repo

Goal: verify the split train archive and list train image members without
copying images into the repository.

Allowed future outputs:

- local-only reassembled train ZIP in the work folder;
- local-only archive listing text/CSV in the work folder;
- tiny repository summary after verification.

Not allowed:

- full extraction into the repo;
- committing raw split files;
- committing reassembled ZIPs;
- committing train images.

### Stage B - Extract Only Tiny Labelled Preview Samples Outside The Repo

Goal: extract at most a tiny source-quality preview outside the repository.

Use `trainLabels.csv` to choose selected image IDs first, then extract only
those JPEGs into the local-only work folder.

### Stage C - Create Small Review-Only Contact Sheets/Index Inside Repo If Needed

Goal: after Stage B succeeds, create a small review-support artifact inside the
repo only if explicitly approved.

Limits:

- 60 preview images maximum;
- contact sheets only, if needed;
- source labels preserved as source labels only;
- no accepted labels;
- no manifest promotion.

### Stage D - Never Train Until Reviewed Evidence Is Created

No training, fitting, challenge manifest, or model/app/runtime change is allowed
from this source until:

1. source access is verified;
2. a review-only sample is visually inspected;
3. candidate rows are manually adjudicated;
4. an explicit evidence-addition proposal is approved;
5. reviewed evidence exists in the canonical reviewed manifest.

## macOS Command Examples For Future Use Only

These commands are examples only. They were not executed while creating this
plan.

Create the local work folder:

```bash
mkdir -p "/Users/bharatsharma/Documents/EyeScan_Local_Data/large_dr_82gb_work/outer_members"
mkdir -p "/Users/bharatsharma/Documents/EyeScan_Local_Data/large_dr_82gb_work/reassembled"
mkdir -p "/Users/bharatsharma/Documents/EyeScan_Local_Data/large_dr_82gb_work/train_listings"
mkdir -p "/Users/bharatsharma/Documents/EyeScan_Local_Data/large_dr_82gb_work/tiny_preview_extract"
```

Copy only train split members outside the repo:

```bash
cd "/Users/bharatsharma/Documents/EyeScan_Local_Data/large_dr_82gb_work/outer_members"
unzip -j "/Volumes/My Passport/Datasets/DR-Diabetic Retinopathy/diabetic-retinopathy-detection.zip" \
  "train.zip.001" "train.zip.002" "train.zip.003" "train.zip.004" "train.zip.005"
```

Copy the label ZIP outside the repo:

```bash
unzip -j "/Volumes/My Passport/Datasets/DR-Diabetic Retinopathy/diabetic-retinopathy-detection.zip" \
  "trainLabels.csv.zip" \
  -d "/Users/bharatsharma/Documents/EyeScan_Local_Data/large_dr_82gb_work/outer_members"
```

Reassemble the train ZIP outside the repo:

```bash
cd "/Users/bharatsharma/Documents/EyeScan_Local_Data/large_dr_82gb_work/outer_members"
cat train.zip.001 train.zip.002 train.zip.003 train.zip.004 train.zip.005 \
  > "../reassembled/train.zip"
```

List archive contents without extracting images:

```bash
zipinfo -1 "/Users/bharatsharma/Documents/EyeScan_Local_Data/large_dr_82gb_work/reassembled/train.zip" \
  > "/Users/bharatsharma/Documents/EyeScan_Local_Data/large_dr_82gb_work/train_listings/train_zip_members.txt"
```

Inspect only the first few member names:

```bash
sed -n '1,40p' \
  "/Users/bharatsharma/Documents/EyeScan_Local_Data/large_dr_82gb_work/train_listings/train_zip_members.txt"
```

Extract only selected files after a tiny preview list is prepared:

```bash
cd "/Users/bharatsharma/Documents/EyeScan_Local_Data/large_dr_82gb_work/tiny_preview_extract"
unzip "/Users/bharatsharma/Documents/EyeScan_Local_Data/large_dr_82gb_work/reassembled/train.zip" \
  "train/15_right.jpeg" "train/99_left.jpeg"
```

If the archive members do not include a `train/` prefix, adjust the selected
member names based on the archive listing before extraction.

## Proposed Preview Sampling Strategy After Safe Image Access

After train image access is verified outside the repo, create a source-quality
preview sample with 60 images maximum:

- 20 `Moderate`
- 10 `Severe`
- 10 `Proliferative_DR`
- 10 `Mild`
- 10 `No_DR`

Purpose: visual source quality inspection only.

This preview must not be treated as accepted evidence. Source severity labels
must remain source labels only.

## Required Guardrails For Future Execution

- No full extraction into the repository.
- No committed raw images unless explicitly limited to a tiny preview/contact
  sheet artifact.
- No committed split ZIP files.
- No committed reassembled ZIP files.
- No `reviewed_manifest_v1.csv` changes during source-access verification.
- No `fitting_manifest_v1.csv` creation.
- No `challenge_manifest_v1.csv` creation.
- No manifest promotion.
- No training.
- No fitting.
- No model, app, backend, runtime, or preserved-package changes.

## Recommended Next Step

Before running any future split-ZIP commands, check available disk space in the
local work location. Then, if explicitly approved, perform Stage A only and
return the train archive listing plus label-to-image mapping verification.
