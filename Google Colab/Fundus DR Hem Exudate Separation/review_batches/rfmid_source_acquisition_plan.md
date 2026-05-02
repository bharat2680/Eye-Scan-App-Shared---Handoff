# RFMiD Source Acquisition Plan

## Purpose

This plan covers the next safe sourcing step for improving the weakest planned
class:

- `hemorrhage_pattern_dominant_non_dr`

Current local exploratory review produced only a very small number of useful
non-DR hemorrhage-dominant candidates, so this class remains underpowered.

The main objective of this plan is to improve
`hemorrhage_pattern_dominant_non_dr` coverage without forcing diabetic
retinopathy folder hemorrhage examples into a non-DR hemorrhage class.

This is acquisition planning only. It does not approve downloads, does not
create fitting manifests, and does not approve training.

## Recommended External Sources

Priority order:

1. `RFMiD` / `RIADD`
   - first priority for color fundus multi-disease sourcing
   - likely best path for finding expert-labelled non-DR vascular examples

2. `RFMiD 2.0`
   - possible supplement if the package includes usable image payload plus CSV
     annotations
   - potentially useful for expanding weak vascular and hemorrhage coverage

3. dedicated `RVO` / `BRVO` / `CRVO` color fundus datasets
   - only if publicly downloadable and clearly color-fundus based
   - should be used as targeted supplements for
     `hemorrhage_pattern_dominant_non_dr`

Explicit exclusion:

- avoid OCT-only RVO datasets for this lane

Reason:

- this lane is a color fundus pattern-separation task
- OCT-only vein-occlusion datasets are not suitable for this color fundus
  objective

## Known Source Facts To Carry Forward

### RFMiD

Known working facts from existing project documentation and prior notes:

- public retinal fundus multi-disease dataset
- `3,200` images
- expert annotations
- `45` disease/pathology categories plus `Disease_Risk`
- split into training, validation, and testing sets
- previously documented local/remote package structure references:
  - `1. Original Images.zip`
  - `a. RFMiD_Training_Labels.csv`
  - `b. RFMiD_Validation_Labels.csv`
  - `c. RFMiD_Testing_Labels.csv`

Source-location note:

- RFMiD / RIADD is referenced by Grand Challenge / RIADD
- RFMiD may also be mirrored on Hugging Face

### RFMiD 2.0

Known working facts to document for later verification:

- around `860` retinal fundus images
- specialist annotated
- multilabel / multiclass framing
- CSV labels expected
- Zenodo is the expected source
- expected license context: `CC BY 4.0`

## Desired Labels And Columns To Check After Mounting Or Downloading

After a candidate source is mounted or placed locally, inspect label CSVs only
before any manifest work.

Highest-priority label or column checks:

- `BRVO`
- `CRVO`
- `RVO`
- `retinal vein occlusion`
- `vein occlusion`
- `hypertensive retinopathy`
- `hemorrhage`
- `haemorrhage`
- `Disease_Risk`
- `WNL`
- `normal`

Interpretation rule:

- source labels should be treated as candidate selectors only
- source labels are not final labels for this five-class lane

## Mount Or Download Decision Rules

Acquisition rules:

- prefer an official source first
- if a previously documented local package already exists, prefer mounting or
  locating that package before downloading a new copy
- do not commit large image payloads into git

Preferred storage locations outside git:

- `/Users/bharatsharma/Documents/EyeScan_Local_Data/datasets/fundus/RFMiD/`
- `/Volumes/My Passport/EyeScan App/Datasets/External Fundus/RFMiD/`

Git rule:

- only small manifests, review batches, notes, and helper docs should be
  committed
- large archives, extracted images, and source payloads should remain outside
  version control

## Next Technical Step After Dataset Is Mounted

Do this in order:

1. inspect label CSVs only
2. verify whether `BRVO`, `CRVO`, `RVO`, hemorrhage-like, vascular, or
   hypertensive-retinopathy-style labels actually exist
3. create a dry-run raw candidate manifest for those source labels only
4. create a small exploratory review batch plus contact sheet
5. stop there until review quality and class coverage are checked

Explicit non-step:

- no training

## Safety Warnings

- source disease labels are only `proposed_label`
- `final_label` must come from visual review
- no `fitting_manifest_v1.csv` until class coverage is reviewed
- no training until explicitly approved
- do not force DR-folder hemorrhage examples into
  `hemorrhage_pattern_dominant_non_dr` just because they look lesion-positive

## Recommended Immediate Next Action

If approval is given later:

1. locate or mount the previously documented RFMiD package first
2. inspect label CSV names and columns
3. confirm whether BRVO/CRVO/RVO-style labels are present
4. only then create an exploratory dry-run raw candidate manifest

Until then:

- no download
- no dataset extraction
- no manifest commit beyond planning notes
