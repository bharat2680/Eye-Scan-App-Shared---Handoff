# RFMiD Local Inspection Report

## Purpose

This note records local inspection only for RFMiD-related files already present
on the external drive.

This is inspection only:

- no ZIP extraction was performed
- no manifest was created
- no training was started

## Actual Inspected Paths

Top-level folder inspected:

- `/Volumes/My Passport/Datasets/External Fundus/`

RFMiD-specific folder inspected:

- `/Volumes/My Passport/Datasets/External Fundus/RFMiD Datasets/`

Files confirmed inside `RFMiD Datasets/`:

- `RFMiD2_0.zip`
- `RFMiD_V_2.1.zip`
- `a. RFMiD_Training_Labels.csv`
- `b. RFMiD_Validation_Labels.csv`
- `c. RFMiD_Testing_Labels.csv`
- `archive (1).zip`

Additional RFMiD-related archive confirmed at the external-fundus root:

- `/Volumes/My Passport/Datasets/External Fundus/1. Original Images.zip`

## RFMiD Label CSV Inspection

### Training labels

Path:

- `/Volumes/My Passport/Datasets/External Fundus/RFMiD Datasets/a. RFMiD_Training_Labels.csv`

Row count:

- `1920`

Columns:

- `ID`
- `Disease_Risk`
- `DR`
- `ARMD`
- `MH`
- `DN`
- `MYA`
- `BRVO`
- `TSLN`
- `ERM`
- `LS`
- `MS`
- `CSR`
- `ODC`
- `CRVO`
- `TV`
- `AH`
- `ODP`
- `ODE`
- `ST`
- `AION`
- `PT`
- `RT`
- `RS`
- `CRS`
- `EDN`
- `RPEC`
- `MHL`
- `RP`
- `CWS`
- `CB`
- `ODPM`
- `PRH`
- `MNF`
- `HR`
- `CRAO`
- `TD`
- `CME`
- `PTCR`
- `CF`
- `VH`
- `MCA`
- `VS`
- `BRAO`
- `PLQ`
- `HPED`
- `CL`

Positive counts for requested columns:

- `Disease_Risk = 1519`
- `DR = 376`
- `BRVO = 73`
- `CRVO = 28`
- `HR = 0`
- `HTN` column not present
- `WNL` column not present
- `NORMAL` column not present

### Validation labels

Path:

- `/Volumes/My Passport/Datasets/External Fundus/RFMiD Datasets/b. RFMiD_Validation_Labels.csv`

Row count:

- `640`

Positive counts for requested columns:

- `Disease_Risk = 506`
- `DR = 132`
- `BRVO = 23`
- `CRVO = 8`
- `HR = 0`
- `HTN` column not present
- `WNL` column not present
- `NORMAL` column not present

### Testing labels

Path:

- `/Volumes/My Passport/Datasets/External Fundus/RFMiD Datasets/c. RFMiD_Testing_Labels.csv`

Row count:

- `640`

Positive counts for requested columns:

- `Disease_Risk = 506`
- `DR = 124`
- `BRVO = 23`
- `CRVO = 9`
- `HR = 1`
- `HTN` column not present
- `WNL` column not present
- `NORMAL` column not present

## Useful Label Columns Found

Confirmed present in the original RFMiD label CSVs:

- `Disease_Risk`
- `DR`
- `BRVO`
- `CRVO`
- `HR`

Not found in the inspected original RFMiD CSVs:

- `HTN`
- `WNL`
- `NORMAL`

## Image Payload Inspection

### `1. Original Images.zip`

Path:

- `/Volumes/My Passport/Datasets/External Fundus/1. Original Images.zip`

ZIP size:

- `7,963,062,839` bytes

Top-level contents:

- `1. Original Images`

Safe image count from ZIP listing:

- `3200`

Observed filename pattern:

- `1. Original Images/a. Training Set/1.png`
- `1. Original Images/a. Training Set/10.png`
- `1. Original Images/a. Training Set/100.png`

Interpretation:

- filenames appear to be numeric IDs
- this looks compatible with the RFMiD label CSV `ID` column

### `RFMiD2_0.zip`

Path:

- `/Volumes/My Passport/Datasets/External Fundus/RFMiD Datasets/RFMiD2_0.zip`

ZIP size:

- `63,658,404` bytes

Top-level contents:

- `Training_set.zip`
- `Validation_set.zip`
- `Test_set.zip`

Safe image count from outer ZIP listing:

- `0` directly visible images in the outer archive

Interpretation:

- this is a nested archive
- no label CSV was visible from the outer ZIP listing in this pass

### `RFMiD_V_2.1.zip`

Path:

- `/Volumes/My Passport/Datasets/External Fundus/RFMiD Datasets/RFMiD_V_2.1.zip`

ZIP size:

- `79,985,246` bytes

Top-level contents:

- `RFMiD_2`

Safe image count from ZIP listing:

- `1844`

Sample paths:

- `RFMiD_2/AH/1.jpg`
- `RFMiD_2/AH/10.jpg`
- `RFMiD_2/AH/11.jpg`

Interpretation:

- this appears to be a folder-organized image archive
- no extracted CSV label file was visible beside it in the inspected folder
- further inspection should wait until approval to inspect that archive more
  deeply

## Extracted Image Presence

Within the visible local `RFMiD Datasets/` folder:

- no extracted original RFMiD image tree was visible
- original RFMiD labels are extracted as CSV files
- image payload is currently present as ZIP archives

## Best Immediate Use For The Weak Class

Most useful confirmed labels for this lane:

- `BRVO`
- `CRVO`

Potentially useful but ambiguous without source documentation:

- `HR`

Immediate practical implication:

- the local RFMiD original label CSVs already provide a credible candidate
  source for `hemorrhage_pattern_dominant_non_dr`

## Recommended Next Step

Recommended next technical step:

- create RFMiD `BRVO` / `CRVO` / `HR` exploratory raw candidate manifest,
  dry-run first

Do not train yet.

## Safety Note

Source labels are `proposed_label` only.

Even if `BRVO`, `CRVO`, or other vascular labels are selected from RFMiD,
`final_label` must still come from visual review before any future fitting
export.
