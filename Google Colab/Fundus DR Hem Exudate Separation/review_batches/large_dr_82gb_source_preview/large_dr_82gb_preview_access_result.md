# Large DR 82GB Preview Access Result

## Scope

This records the attempted Stage A/B preview access run for the large Kaggle
Diabetic Retinopathy Detection source.

No training was performed. No fitting was performed. No reviewed, fitting, or
challenge manifests were created or modified. No app, backend, runtime, model,
or preserved-package files were changed.

## Intended Source

- External archive path:
  `/Volumes/My Passport/Datasets/DR-Diabetic Retinopathy/diabetic-retinopathy-detection.zip`
- Allowed local-only work folder:
  `/Users/bharatsharma/Documents/EyeScan_Local_Data/large_dr_82gb_work/`

## Local Work Folder

Created the local-only work folder structure outside the repository:

- `/Users/bharatsharma/Documents/EyeScan_Local_Data/large_dr_82gb_work/outer_members/`
- `/Users/bharatsharma/Documents/EyeScan_Local_Data/large_dr_82gb_work/reassembled/`
- `/Users/bharatsharma/Documents/EyeScan_Local_Data/large_dr_82gb_work/train_listings/`
- `/Users/bharatsharma/Documents/EyeScan_Local_Data/large_dr_82gb_work/tiny_preview_extract/`

No large files were written to these folders during this attempt.

## Access Result

Train image access did not work in this run.

Reason:

- `/Volumes/My Passport/Datasets/DR-Diabetic Retinopathy/diabetic-retinopathy-detection.zip`
  was not visible.
- `/Volumes` showed only `Macintosh HD` and `WD Unlocker`.
- `diskutil` showed the external device as the small read-only `WD Unlocker`
  volume, not the unlocked data volume containing the dataset.
- A filesystem search under `/Volumes`, Desktop, Downloads, and Documents did
  not find `diabetic-retinopathy-detection.zip`.

Additional safety blocker:

- The local `/Users/bharatsharma/Documents` volume had about 16 GiB free.
- The planned reassembled train ZIP is expected to require about 32.6 GiB before
  any image extraction.
- This is below the recommended 200-250 GiB free-space guardrail.

Because of these blockers, Stage A stopped before reassembly or listing.

## Stage A Outcome

- Local work folder created: yes.
- Source archive found at expected mounted path: no.
- Train split files copied: no.
- Train split ZIP reassembled: no.
- Train ZIP listed: no.
- Label-to-image mapping verified from train ZIP: no.

## Stage B Outcome

- Preview images extracted: 0.
- Preview contact sheets created: 0.
- `large_dr_82gb_preview_index_stage_b.csv` created as a header-only placeholder
  to document that no rows were accessible in this run.

Requested target sample remains pending until the archive is available and
enough local scratch space is available:

- 20 `Moderate`
- 10 `Severe`
- 10 `Proliferative_DR`
- 10 `Mild`
- 10 `No_DR`
- 60 preview images maximum

## Safety Confirmation

- No full extraction into the repository occurred.
- No large raw images were copied into the repository.
- No reassembled ZIP was created inside the repository.
- No accepted labels were created.
- No review bucket labels were created.
- No rows were added to `reviewed_manifest_v1.csv`.
- No `fitting_manifest_v1.csv` was created.
- No `challenge_manifest_v1.csv` was created.
- No training/model/app/backend/runtime/preserved-package changes were made.

## Required Before Retrying

Before retrying Stage A/B:

1. Unlock and mount the external `My Passport` data volume so the archive is
   visible at `/Volumes/My Passport/Datasets/DR-Diabetic Retinopathy/`.
2. Use a local-only work location with at least 200-250 GiB free space, or
   choose a different approved external scratch location outside the repository.
3. Re-run Stage A only after confirming the archive path and free-space
   guardrails.
