# Large DR 82GB Windows Preview Access Result

Generated: 2026-05-04 17:37:35

## Scope

This is a tiny train-image preview pack only. No training, fitting, app/backend/runtime/model changes, preserved package changes, test image processing, or full dataset extraction was performed.

## Access Checks

- `F:\` writable: yes, confirmed with a create/read/delete probe in `F:\EyeScan_Local_Data\large_dr_82gb_work\`.
- Free space before preview work: 406,034,305,024 bytes (378.15 GiB).
- Free space after selected extraction and temporary cleanup: 405,967,400,960 bytes (378.09 GiB).
- 7-Zip available: yes, `C:\Program Files\7-Zip\7z.exe`, version 26.00.
- Outer archive: `F:\Datasets\DR-Diabetic Retinopathy\diabetic-retinopathy-detection.zip`.
- `trainLabels.csv` readable: yes, extracted only `trainLabels.csv.zip` and `trainLabels.csv` into the external work folder.
- `train.zip.001` through `train.zip.005` accessible: yes, listed in the outer archive and reassembled successfully.

## Method Used

Direct nested selected-file extraction from the outer ZIP was attempted for `train.zip.001`, but 7-Zip reported that the nested path was invalid. The fallback method was used.

- Method: temporary reassembly of `train.zip` inside `F:\EyeScan_Local_Data\large_dr_82gb_work\`, then selected-file extraction only.
- Temporary `train.zip` created: yes, 34,988,445,506 bytes.
- Free space while temporary `train.zip` existed, immediately before deletion: 370,978,955,264 bytes (345.50 GiB).
- Temporary `train.zip` deleted after selected extraction: yes.
- Full train extraction: no.
- Test image processing: no.

## Preview Output

- External preview image folder: `F:\EyeScan_Local_Data\large_dr_82gb_work\preview_images`.
- External preview JPEG count: 60.
- External preview JPEG bytes: 66,198,752.
- Repo index: `large_dr_82gb_preview_index_windows_stage_b.csv`.
- Repo contact sheet: `large_dr_82gb_windows_preview_contact_sheet_001.jpg`.
- Repo contact sheet: `large_dr_82gb_windows_preview_contact_sheet_002.jpg`.

## Preview Count By Source Severity

- Moderate: 20
- Severe: 10
- Proliferative_DR: 10
- Mild: 10
- No_DR: 10

## Verification Notes

- Preview index rows: 60 (max 60).
- `reviewed_manifest_v1.csv`: not found in this checkout, so the requested 98-row count could not be directly confirmed here.
- `fitting_manifest_v1.csv`: absent.
- `challenge_manifest_v1.csv`: absent.
- Labels shown are source labels only. No accepted labels and no review_bucket labels are included.
- No raw preview JPEGs were copied into the repo; only contact sheets, index, and this note were created in the repo.
- `app`, `backend`, `runtime`, `model`, and `packages`: no repo changes detected.
