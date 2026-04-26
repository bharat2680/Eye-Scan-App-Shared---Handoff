# Dataset Mapping

Last updated: 2026-03-23 02:08 AEDT

## Current local source for anterior specialists

Source:

- `F:\datasets\Image Dataset on Eye Diseases Classification.zip`

Raw labels available:

- `cataract`
- `conjunctivitis`
- `eyelid`
- `normal`
- `pterygium`
- `uveitis`

## Current routed use in the live app

- `anterior_quality_gate_v1` runs first on the Mac side
- `anterior_surface_binary_v2_simplecnn` separates:
  - `normal_surface`
  - `surface_abnormal`
- `anterior_conjunctivitis_vs_normal_v1_simplecnn` now runs after
  `surface_abnormal`
- `anterior_cataract_vs_normal_v1_simplecnn` runs only after `normal_surface`

This means the current local dataset should now be used to split the
`surface_abnormal` bucket into narrower evaluation-only specialists instead of
building another all-anterior classifier.

## Additional local source now prepared for quality-gate work

### `anterior_quality_gate_v2_teyeds`

- source root:
  `C:\Users\HP\OneDrive\Documents\Playground\datasets\teyeds_quality_gate_v1`
- derived labels:
  `good_capture`, `needs_recapture`
- split counts:
  train `561 / 350`
  val `120 / 75`
  test `120 / 75`
- current role:
  Dell-side replacement candidate for the current Mac quality gate
- current artifact status:
  `evaluation_only`, packaged for Mac review
- caution:
  labels are derived from TEyeDS visibility-validity annotations, so this is a
  recapture proxy rather than a perfect match for real EyeScan smartphone
  capture failures

### `eye_vs_non_eye_v1`

- source mix:
  existing anterior image archive for `eye` plus sampled personal-photo
  negatives from the F-drive `2017` through `2025`, `Google Photos`, and
  `Old Pics` folders for `non_eye`
- derived labels:
  `eye`, `non_eye`
- split counts:
  train `1680 / 1609`
  val `360 / 345`
  test `360 / 345`
- current role:
  Dell-side pre-pipeline blocker candidate to stop obvious non-eye images
  before the anterior screening flow
- current artifact status:
  `evaluation_only`, packaged for Mac review
- caution:
  non-eye negatives come from weakly curated personal-photo folders rather than
  a dedicated benchmark, and one corrupt JPEG was removed from the test split
  before final checkpoint evaluation

## Derived task-specific views now available

### `anterior_surface_binary_v1`

- positive:
  `conjunctivitis`, `pterygium`, `uveitis`
- negative:
  `normal`
- excluded:
  `cataract`, `eyelid`
- current role:
  first surface-abnormal router

### `anterior_conjunctivitis_vs_normal_v1`

- positive:
  `conjunctivitis`
- negative:
  `normal`
- counts:
  train `249 / 455`
  val `54 / 97`
  test `54 / 97`
- current role:
  first integrated surface-specific bootstrap specialist
- current artifact status:
  `evaluation_only`, integrated on Mac after `surface_abnormal`

### `anterior_uveitis_vs_normal_v1`

- positive:
  `uveitis`
- negative:
  `normal`
- counts:
  train `157 / 455`
  val `33 / 97`
  test `33 / 97`
- current role:
  next inflammatory-looking surface specialist after conjunctivitis
- current artifact status:
  `evaluation_only`, packaged for Mac review
- caution:
  label quality may be noisy and visually overlap with other red-eye causes

### `anterior_pterygium_vs_normal_v1`

- positive:
  `pterygium`
- negative:
  `normal`
- counts:
  train `72 / 455`
  val `15 / 97`
  test `15 / 97`
- current role:
  longer-shot surface specialist candidate
- current artifact status:
  `evaluation_only`, packaged for Mac review
- caution:
  current positive count is very small, so treat this as evaluation-only until
  more curated data is added

### `anterior_eyelid_abnormality_vs_normal_v1`

- positive:
  `eyelid`
- negative:
  `normal`
- counts:
  train `367 / 455`
  val `79 / 97`
  test `79 / 97`
- current role:
  optional separate branch if eyelid disease remains in product scope
- current artifact status:
  `evaluation_only`, packaged but not recommended as a default surface follow-on
- caution:
  this is not a clean replacement for the current surface-positive branch

### `anterior_cataract_vs_normal_v1`

- positive:
  `cataract`
- negative:
  `normal`
- current role:
  cataract specialist after `normal_surface`
- current artifact status:
  `evaluation_only`, integrated on Mac after `normal_surface`

## Interpretation guidance

- `surface_abnormal` should stay a router or fallback label, not a final
  diagnosis label
- `conjunctivitis_vs_normal` is already the first narrow surface-specific head
  in the live app
- `uveitis_vs_normal` is the strongest next Dell-side candidate to review after
  conjunctivitis
- `pterygium_vs_normal` is promising but data-limited
- `eyelid_abnormality_vs_normal` should only be promoted if the product still
  wants eyelid findings in scope

## Fundus note for this pass

- local fundus manifests and artifacts still exist in this workspace
- they are not the current app-facing priority while the surface-positive
  anterior branch is being made more specific

## Prepared external fundus staging paths

These are the exact curated folder roots now expected by the external manifest
prep script:

### `fundus_dr_idrid_v1`

- exact dataset path:
  `F:\datasets\External Fundus\IDRiD_DR_vs_Healthy`
- current Mac/Desktop staging path:
  `/Users/bharatsharma/Desktop/Eye Scan App Handoff/Datasets 2026/External Fundus/IDRiD_DR_vs_Healthy`
- expected raw folders under that path:
  `Diabetic Retinopathy`, `Healthy`
- exact manifest path:
  `C:\Users\HP\OneDrive\Documents\Playground\datasets\manifests\fundus_dr_idrid_v1.jsonl`
- exact config path:
  `C:\Users\HP\OneDrive\Documents\Playground\configs\fundus_dr_idrid_v1_simplecnn.json`
- exact artifact path:
  `C:\Users\HP\OneDrive\Documents\Playground\artifacts\fundus\fundus_dr_idrid_v1_simplecnn`
- label map:
  `Diabetic Retinopathy -> diabetic_retinopathy`, `Healthy -> healthy`
- preprocessing contract:
  RGB, `224 x 224`, direct resize, `float32`, model contains internal
  `Rescaling(1.0 / 255.0)`
- threshold strategy:
  threshold-tuned binary decision on `p(diabetic_retinopathy)`
- current staged counts on the Mac:
  `348` diabetic retinopathy, `168` healthy
- deployment status:
  `pending_dataset`

### `fundus_glaucoma_refuge_v1`

- exact dataset path:
  `F:\datasets\External Fundus\REFUGE_Glaucoma_vs_Healthy`
- expected raw folders under that path:
  `Glaucoma`, `Healthy`
- exact manifest path:
  `C:\Users\HP\OneDrive\Documents\Playground\datasets\manifests\fundus_glaucoma_refuge_v1.jsonl`
- exact config path:
  `C:\Users\HP\OneDrive\Documents\Playground\configs\fundus_glaucoma_refuge_v1_simplecnn.json`
- exact artifact path:
  `C:\Users\HP\OneDrive\Documents\Playground\artifacts\fundus\fundus_glaucoma_refuge_v1_simplecnn`
- label map:
  `Glaucoma -> glaucoma`, `Healthy -> healthy`
- preprocessing contract:
  RGB, `224 x 224`, direct resize, `float32`, model contains internal
  `Rescaling(1.0 / 255.0)`
- threshold strategy:
  threshold-tuned binary decision on `p(glaucoma)`
- current note:
  official REFUGE download is still access-gated, so no matching staged folder
  has been prepared on the Mac/Desktop handoff yet
- deployment status:
  `pending_dataset`

## Newly inspected external fundus archives

### `Eye-Fundus.zip`

- exact dataset path:
  `F:\Datasets\External Fundus\Eye-Fundus.zip`
- inspected structure:
  `train`, `valid`, and `test` class folders already encoded inside the zip
- inspected labels:
  `Central Serous Chorioretinopathy`, `Diabetic Retinopathy`, `Disc Edema`,
  `Glaucoma`, `Healthy`, `Macular Scar`, `Myopia`, `Pterygium`,
  `Retinal Detachment`, `Retinitis Pigmentosa`
- inspected scale:
  `16,242` total images
- sample image size:
  `224 x 224`
- recommended derived tasks:
  `diabetic_retinopathy_vs_healthy`, `glaucoma_vs_healthy`
- deployment status:
  `usable_fallback_dataset`
- caution:
  some internal label-folder names include trailing spaces, so label cleanup is
  required during manifest prep

### `RFMiD2_0.zip`

- exact dataset path:
  `F:\Datasets\External Fundus\RFMiD2_0.zip`
- inspected structure:
  outer archive contains only `Training_set.zip`, `Validation_set.zip`, and
  `Test_set.zip`
- inspected image counts:
  train `509`, val `177`, test `174`
- sample image size:
  `512 x 512`
- deployment status:
  `incomplete_download`
- blocker:
  the current archive does not include a label CSV or annotation file

### `1. Original Images.zip`

- exact dataset path:
  `F:\Datasets\External Fundus\1. Original Images.zip`
- inspected structure:
  `a. Training Set`, `b. Validation Set`, `c. Testing Set`
- inspected split counts:
  train `1,920`, val `640`, test `640`
- sample image size:
  `2144 x 1424`
- likely identity:
  RFMiD original image payload
- deployment status:
  `trainable_multilabel_package`
- matching ground-truth files:
  `F:\Datasets\External Fundus\a. RFMiD_Training_Labels.csv`
  `F:\Datasets\External Fundus\b. RFMiD_Validation_Labels.csv`
  `F:\Datasets\External Fundus\c. RFMiD_Testing_Labels.csv`
- label shape:
  `47` columns total with `45` disease label columns plus `Disease_Risk`

### `archive (1).zip`

- exact dataset path:
  `F:\Datasets\External Fundus\archive (1).zip`
- inspected structure:
  contains only `All ARMD images`
- inspected scale:
  `511` PNG images
- sample image size:
  `300 x 300`
- deployment status:
  `separate_armd_archive`
- blocker:
  not the missing RFMiD labels and not a broad multi-disease metadata file

### `fundus_glaucoma_papila_v1`

- exact dataset path:
  `F:\datasets\External Fundus\PAPILA_Glaucoma_vs_Healthy`
- current Mac/Desktop staging path:
  `/Users/bharatsharma/Desktop/Eye Scan App Handoff/Datasets 2026/External Fundus/PAPILA_Glaucoma_vs_Healthy`
- expected raw folders under that path:
  `Glaucoma`, `Healthy`
- exact manifest path:
  `C:\Users\HP\OneDrive\Documents\Playground\datasets\manifests\fundus_glaucoma_papila_v1.jsonl`
- exact config path:
  `C:\Users\HP\OneDrive\Documents\Playground\configs\fundus_glaucoma_papila_v1_simplecnn.json`
- exact artifact path:
  `C:\Users\HP\OneDrive\Documents\Playground\artifacts\fundus\fundus_glaucoma_papila_v1_simplecnn`
- label map:
  `Glaucoma -> glaucoma`, `Healthy -> healthy`
- preprocessing contract:
  RGB, `224 x 224`, direct resize, `float32`, model contains internal
  `Rescaling(1.0 / 255.0)`
- threshold strategy:
  threshold-tuned binary decision on `p(glaucoma)`
- current staged counts on the Mac:
  `87` glaucoma, `333` healthy, with `68` suspicious cases excluded from the
  binary folder prep
- deployment status:
  `pending_dataset`

## Prepared foundation-model staging paths

These are not manifests yet. They are the exact weight files now recommended
for download so the next training wave can compare official pretrained
ophthalmic backbones against the local baselines.

Latest verifier result:

- ran:
  `python scripts/check_foundation_model_staging.py`
- result:
  `0 / 4` present
- exact blocker:
  `F:\datasets\FoundationModels` does not exist yet

### `visionfm_external_eye`

- exact staged weight path:
  `F:\datasets\FoundationModels\VisionFM\ExternalEye\visionfm_external_eye.pth`
- intended use:
  next best pretrained backbone candidate for `anterior_quality_gate`,
  `anterior_surface_binary`, `conjunctivitis`, `uveitis`, and `pterygium`
- deployment status:
  `pending_download`

### `visionfm_slit_lamp`

- exact staged weight path:
  `F:\datasets\FoundationModels\VisionFM\SlitLamp\visionfm_slit_lamp.pth`
- intended use:
  comparison backbone for cataract and surface-specialist refinement
- deployment status:
  `pending_download`

### `retfound_dinov2_meh`

- exact staged weight path:
  `F:\datasets\FoundationModels\RETFound\Fundus\retfound_dinov2_meh.pth`
- intended use:
  official pretrained fundus backbone for the next external-data DR and
  glaucoma wave
- deployment status:
  `pending_download`

### `visionfm_fundus`

- exact staged weight path:
  `F:\datasets\FoundationModels\VisionFM\Fundus\visionfm_fundus.pth`
- intended use:
  second official fundus backbone to compare against `RETFound`
- deployment status:
  `pending_download`
