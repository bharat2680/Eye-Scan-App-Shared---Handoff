# Hemorrhage Non-DR Source Investigation

## Purpose

This note records a targeted local source search for the weakest planned class:

- `hemorrhage_pattern_dominant_non_dr`

This is source investigation only. It does not approve training, does not
create a fitting manifest, and does not download any new data.

## Searched Paths

Targeted local and documented paths searched:

- `/Volumes/My Passport/EyeScan App/Datasets/`
- `/Users/bharatsharma/Documents/EyeScan_Local_Data/datasets/fundus/`
- `/Users/bharatsharma/Documents/EyeScan_Local_Data/`
- `/Users/bharatsharma/Desktop/`
- repo docs and manifests under:
  - `docs/`
  - `Google Colab/Fundus DR Hem Exudate Separation/`
  - `/Users/bharatsharma/Documents/EyeScan_Local_Data/datasets/fundus/broad_abnormality_v1/`

Search terms used:

- `RFMiD`
- `RFMiD2`
- `RIADD`
- `BRVO`
- `CRVO`
- `RVO`
- `retinal vein occlusion`
- `vein occlusion`
- `vascular`
- `hemorrhage`
- `haemorrhage`
- `hypertensive retinopathy`

## Sources Found Locally

### 1. Small manual exploratory source

Visible local folder:

- `/Users/bharatsharma/Desktop/Eye Images Test/Fundus Images`

Visible scale:

- `12` image files

Why it matters:

- older local curation metadata references this folder with notes such as
  `retinal_hemorrhage_candidate`
- the same metadata also references
  `vascular_or_structural_uncertain`

Limitations:

- this is not a clean dedicated non-DR vascular dataset
- provenance is manual/local rather than a curated disease benchmark
- this source only yielded a very small exploratory hemorrhage non-DR batch

Conclusion:

- useful for exploratory review only
- not sufficient as the primary source for
  `hemorrhage_pattern_dominant_non_dr`

### 2. Broad-abnormality metadata references

Visible local metadata:

- `/Users/bharatsharma/Documents/EyeScan_Local_Data/datasets/fundus/broad_abnormality_v1/reviewed_manifest.csv`
- `/Users/bharatsharma/Documents/EyeScan_Local_Data/datasets/fundus/broad_abnormality_v1/reviewed_counts_summary.md`
- `/Users/bharatsharma/Documents/EyeScan_Local_Data/datasets/fundus/broad_abnormality_v1/manual_review_checklist.md`

Relevant labels found in metadata:

- `hemorrhage_exudate_like`
- `vascular_non_glaucoma`

Useful implication:

- prior work already recognized a vascular/non-glaucoma bucket
- that metadata may help identify exploratory examples

Limitation:

- this is not the same as a clean RFMiD / BRVO / CRVO / RVO source
- prior broad labels are too coarse to substitute for a dedicated
  non-DR hemorrhage dataset

### 3. RFMiD documented elsewhere, but not locally visible here

Repo docs reference RFMiD assets on a different machine path:

- `F:\\Datasets\\External Fundus\\RFMiD2_0.zip`
- `F:\\Datasets\\External Fundus\\1. Original Images.zip`
- `F:\\Datasets\\External Fundus\\a. RFMiD_Training_Labels.csv`
- `F:\\Datasets\\External Fundus\\b. RFMiD_Validation_Labels.csv`
- `F:\\Datasets\\External Fundus\\c. RFMiD_Testing_Labels.csv`

Observed from repo documentation only:

- RFMiD image payload and matching label CSVs were documented previously
- label files were described as having `47` columns total with `45` disease
  label columns plus `Disease_Risk`

Important limitation:

- these files are not visible in the currently accessible local Mac dataset
  roots from this investigation pass
- no local RFMiD label CSV was opened here, so BRVO/CRVO/RVO columns were not
  directly verified from a local file in this session

## Sources Not Found Locally

No clearly visible local source was found in the searched Mac-accessible roots
for:

- RFMiD image payload with locally accessible label CSVs
- RFMiD 2.0 with usable local annotation CSVs
- RIADD
- dedicated BRVO color fundus dataset
- dedicated CRVO color fundus dataset
- dedicated RVO color fundus dataset
- dedicated retinal vein occlusion or hypertensive-retinopathy fundus folder

## Recommended External Dataset Candidates

Recommended candidates for approval before any download:

1. `RFMiD` / `RIADD`
   - expert-labelled color fundus disease datasets
   - strong candidates because BRVO-like or vascular disease labels may exist
   - best first external source to verify

2. `RFMiD 2.0`
   - possible supplement if complete image payload plus annotation CSVs are
     available
   - especially useful if vascular disease labels are expanded or cleaner

3. dedicated `RVO` / `BRVO` / `CRVO` color fundus datasets
   - useful if they are publicly downloadable and clearly color-fundus based
   - should be preferred over OCT-only vein-occlusion datasets for this lane

## Important Modality Note

OCT-only RVO datasets are not suitable for this color fundus lane.

This lane is specifically about color fundus pattern separation, so future
sourcing should prioritize color fundus images with reliable lesion or disease
labels.

## Recommendation

Current conclusion:

- no clean local RFMiD / BRVO / CRVO / RVO color-fundus source was confirmed in
  the currently accessible Mac-visible roots
- the strongest local evidence remains the tiny manual exploratory folder plus
  older broad-abnormality vascular metadata

Recommended next step if approval is given later:

- obtain or mount the previously documented RFMiD package if it is accessible
  from current storage
- then create an RFMiD BRVO exploratory raw candidate manifest, dry-run first

## Download Safety

No download should occur until explicitly approved.
