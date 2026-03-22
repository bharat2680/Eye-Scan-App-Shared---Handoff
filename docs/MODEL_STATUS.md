# Model Status

Last updated: 2026-03-22 22:39 AEDT

## Current integrated anterior app pipeline

1. `anterior_quality_gate_v1`
2. `anterior_surface_binary_v2_simplecnn`
3. `anterior_conjunctivitis_vs_normal_v1_simplecnn` only after `surface_abnormal`
4. `anterior_uveitis_vs_normal_v1_simplecnn` only after `surface_abnormal`
   and only when conjunctivitis stays negative
5. `anterior_pterygium_vs_normal_v1_simplecnn` only after `surface_abnormal`
   and only when both conjunctivitis and uveitis stay negative
6. `anterior_cataract_vs_normal_v1_simplecnn` only after `normal_surface`

## Current integrated anterior artifacts

### `anterior_surface_binary_v2_simplecnn`

- exact dataset path:
  `F:\datasets\Image Dataset on Eye Diseases Classification.zip`
- exact manifest path:
  `C:\Users\HP\OneDrive\Documents\Playground\datasets\manifests\anterior_surface_binary_v1.jsonl`
- exact config path:
  `C:\Users\HP\OneDrive\Documents\Playground\configs\anterior_surface_binary_v2_simplecnn.json`
- exact artifact path:
  `C:\Users\HP\OneDrive\Documents\Playground\artifacts\anterior\anterior_surface_binary_v2_simplecnn`
- label map:
  `normal_surface -> 0`, `surface_abnormal -> 1`
- preprocessing contract:
  RGB, `224 x 224`, direct resize, `float32`, model contains internal
  `Rescaling(1.0 / 255.0)`
- threshold strategy:
  plain `argmax`
- validation metrics:
  `val_accuracy=0.9849`, `val_loss=0.0611`
- test metrics:
  `test_accuracy=0.9950`
  confusion matrix `[[96, 1], [0, 102]]`
- deployment status:
  `evaluation_only`
- intended use:
  first routed specialist after the anterior quality gate
- known failure modes:
  surface-positive output still merges several non-cataract anterior findings
  and should not be shown as a diagnosis

### `anterior_cataract_vs_normal_v1_simplecnn`

- exact dataset path:
  `F:\datasets\Image Dataset on Eye Diseases Classification.zip`
- exact manifest path:
  `C:\Users\HP\OneDrive\Documents\Playground\datasets\manifests\anterior_cataract_vs_normal_v1.jsonl`
- exact config path:
  `C:\Users\HP\OneDrive\Documents\Playground\configs\anterior_cataract_vs_normal_v1_simplecnn.json`
- exact artifact path:
  `C:\Users\HP\OneDrive\Documents\Playground\artifacts\anterior\anterior_cataract_vs_normal_v1_simplecnn`
- label map:
  `cataract -> 0`, `normal -> 1`
- preprocessing contract:
  RGB, `224 x 224`, direct resize, `float32`, model contains internal
  `Rescaling(1.0 / 255.0)`
- threshold strategy:
  threshold-tuned binary decision on the `cataract` score with
  `selected_threshold=0.15`
- validation metrics:
  best checkpoint `val_accuracy=0.8958`, `val_loss=0.2602`
  threshold-tuned `balanced_accuracy=0.9273`
- test metrics:
  default `test_accuracy=0.9553`
  default confusion matrix `[[75, 7], [1, 96]]`
  threshold-tuned `test_accuracy=0.9609`
  threshold-tuned confusion matrix `[[80, 2], [5, 92]]`
- deployment status:
  `evaluation_only`
- intended use:
  run only after `normal_surface`
- known failure modes:
  trained on one local source only and not validated on an external clinical
  holdout

### `anterior_conjunctivitis_vs_normal_v1_simplecnn`

- exact dataset path:
  `F:\datasets\Image Dataset on Eye Diseases Classification.zip`
- exact manifest path:
  `C:\Users\HP\OneDrive\Documents\Playground\datasets\manifests\anterior_conjunctivitis_vs_normal_v1.jsonl`
- exact config path:
  `C:\Users\HP\OneDrive\Documents\Playground\configs\anterior_conjunctivitis_vs_normal_v1_simplecnn.json`
- exact artifact path:
  `C:\Users\HP\OneDrive\Documents\Playground\artifacts\anterior\anterior_conjunctivitis_vs_normal_v1_simplecnn`
- packaged handoff path:
  `C:\Users\HP\OneDrive\Documents\Playground\handoff\macbook_next_specialist_packages\anterior_conjunctivitis_vs_normal_v1_simplecnn_package`
- label map:
  `conjunctivitis -> 0`, `normal -> 1`
- preprocessing contract:
  RGB, `224 x 224`, direct resize, `float32`, model contains internal
  `Rescaling(1.0 / 255.0)`
- threshold strategy:
  threshold-tuned binary decision on the `conjunctivitis` score with
  `selected_threshold=0.15`
- validation metrics:
  best checkpoint `val_accuracy=0.9875`, `val_loss=0.0920`
  threshold-tuned `balanced_accuracy=0.9897`
- test metrics:
  default `test_accuracy=0.9669`
  default confusion matrix `[[49, 5], [0, 97]]`
  threshold-tuned `test_accuracy=0.9934`
  threshold-tuned confusion matrix `[[53, 1], [0, 97]]`
- deployment status:
  `evaluation_only`
- intended use:
  run only after `surface_abnormal` so the app can narrow some broad
  surface-positive results to `Possible conjunctivitis pattern detected`
- known failure modes:
  single-source bootstrap training only and likely overlap with other red-eye
  causes not labeled separately here

## Newer anterior specialist artifacts

### `anterior_quality_gate_v2_teyeds_simplecnn`

- exact dataset path:
  `C:\Users\HP\OneDrive\Documents\Playground\datasets\teyeds_quality_gate_v1`
- exact manifest path:
  `C:\Users\HP\OneDrive\Documents\Playground\datasets\manifests\anterior_quality_gate_v2_teyeds.jsonl`
- exact config path:
  `C:\Users\HP\OneDrive\Documents\Playground\configs\anterior_quality_gate_v2_teyeds_simplecnn.json`
- exact artifact path:
  `C:\Users\HP\OneDrive\Documents\Playground\artifacts\anterior\anterior_quality_gate_v2_teyeds_simplecnn`
- packaged handoff path:
  `C:\Users\HP\OneDrive\Documents\Playground\handoff\macbook_quality_gate_packages\anterior_quality_gate_v2_teyeds_simplecnn_package`
- label map:
  `good_capture -> 0`, `needs_recapture -> 1`
- preprocessing contract:
  RGB, `224 x 224`, direct resize, `float32`, model contains internal
  `Rescaling(1.0 / 255.0)`
- threshold strategy:
  threshold-tuned binary decision on the `needs_recapture` score with
  `selected_threshold=0.35`
- validation metrics:
  best checkpoint `val_accuracy=0.8413`, `val_loss=0.4544`
  threshold-tuned `balanced_accuracy=0.8100`
- test metrics:
  default `test_accuracy=0.8256`
  default confusion matrix `[[111, 9], [25, 50]]`
  threshold-tuned `test_accuracy=0.8103`
  threshold-tuned confusion matrix `[[102, 18], [19, 56]]`
- deployment status:
  `evaluation_only`
- intended use:
  candidate replacement for the current anterior quality gate before
  downstream routing
- known failure modes:
  trained from TEyeDS validity-derived labels rather than your app's own
  recapture decisions, and the negative class is mostly visibility failure
  rather than every possible smartphone capture problem

### `anterior_quality_gate_v3_visionfm_external_linearprobe`

- exact dataset path:
  `/content/drive/MyDrive/Datasets/teyeds_quality_gate_v1.zip`
- exact runtime dataset root:
  `/content/eyescan_colab/datasets/teyeds_quality_gate_v1`
- exact notebook path:
  `Google Colab/Quality Gate/anterior_quality_gate_v3_visionfm_external_linearprobe.ipynb`
- exact backbone path:
  `/content/drive/MyDrive/Datasets/VFM Datasets/VFM_External_weights.pth`
- exact artifact path:
  `/content/drive/MyDrive/EyeScan_Models/VisionFM_Quality_Gate_V3`
- preferred Mac handoff path:
  `F:\EyeScan App\Datasets\VisionFM_Quality_Gate_V3_mac_handoff.zip`
- full package path:
  `F:\EyeScan App\Datasets\VisionFM_Quality_Gate_V3_package.zip`
- label map:
  `good_capture -> 0`, `needs_recapture -> 1`
- preprocessing contract:
  RGB, `224 x 224`, VisionFM external-eye normalization mean
  `[0.4936253, 0.36324808, 0.25956994]`, std
  `[0.32001, 0.27109432, 0.21991591]`
- threshold strategy:
  threshold-tuned binary decision on the `needs_recapture` score with
  `selected_threshold=0.25`
- validation metrics:
  best checkpoint `val_loss=0.1930`
  default `val_accuracy=0.9179`
  threshold-tuned `balanced_accuracy=0.9533`
- test metrics:
  default `test_accuracy=0.9133`
  default confusion matrix `[[110, 11], [6, 69]]`
  threshold-tuned `test_accuracy=0.9337`
  threshold-tuned confusion matrix `[[108, 13], [0, 75]]`
- deployment status:
  `evaluation_only`
- intended use:
  first VisionFM-backed comparison candidate against the current anterior
  quality gate
- known failure modes:
  this Colab run used a fresh local train/val/test split of the TEyeDS-derived
  quality folder, so it is not a strict apples-to-apples replacement study
  against `anterior_quality_gate_v2_teyeds_simplecnn`

### `visionfm_quality_gate_pilot_refined`

- reproducible notebook path on the Mac:
  `/Users/bharatsharma/Desktop/Google Console/Vision FM Files/VisionFM_Pilot.ipynb`
- base checkpoint path:
  `/content/drive/MyDrive/Datasets/VFM Datasets/VFM_External_weights.pth`
- refined classifier path:
  `/content/drive/MyDrive/EyeScan_Models/visionfm_quality_classifier_refined.pkl`
- refined label map path:
  `/content/drive/MyDrive/EyeScan_Models/visionfm_quality_label_map_refined.json`
- labeled metadata path:
  `/content/drive/MyDrive/EyeScan_Models/visionfm_quality_metadata_labeled.csv`
- handoff summary path:
  `/content/drive/MyDrive/EyeScan_Models/visionfm_quality_handoff_summary.json`
- optional reference outputs:
  `/content/drive/MyDrive/EyeScan_Models/outputs/visionfm_teyed_smoke_test/`
- pipeline type:
  `two_stage_pilot`
- label map:
  `bad`, `glare_lighting`, `good_centered`, `off_angle`
- intended use:
  VisionFM-based anterior quality-gate pilot built from TEyeD extracted images
  using VisionFM embeddings plus a LogisticRegression classifier
- deployment status:
  `pilot_review_only`
- integration status:
  do not integrate into `erica_server.py` or the live Mac backend yet
- known caveats:
  this is not a single standalone `.keras` drop-in model, it depends on the
  VisionFM backbone checkpoint plus the refined sklearn classifier, and it
  should use only the refined label map
- notebook-confirmed pipeline:
  TEyeD image embedding extraction -> unsupervised cluster review ->
  refined label assignment -> LogisticRegression classifier export
- shared-lane caveat:
  this does not by itself clear the Dell-side foundation-model staging blocker
  until the underlying `.pth` checkpoint is staged and verified in the
  expected shared path

## Requested next artifact

### `anterior_eye_presence_gate_v1`

- status:
  `requested_next`
- intended use:
  hard-reject obvious non-eye captures before the live quality gate
- preferred labels:
  `eye_present`, `non_eye`
- preferred negative set:
  laptops, monitors, keyboards, screens, phones, tablets, circular toys,
  balls, planets, stars, moon-like imagery, water reflections, printed eyes,
  and on-screen eye photos
- practical reason:
  the Mac-side heuristic hardening improved the false-positive issue, but a
  dedicated learned eye-presence rejector is the cleaner next defense

### `anterior_uveitis_vs_normal_v1_simplecnn`

- exact dataset path:
  `F:\datasets\Image Dataset on Eye Diseases Classification.zip`
- exact manifest path:
  `C:\Users\HP\OneDrive\Documents\Playground\datasets\manifests\anterior_uveitis_vs_normal_v1.jsonl`
- exact config path:
  `C:\Users\HP\OneDrive\Documents\Playground\configs\anterior_uveitis_vs_normal_v1_simplecnn.json`
- exact artifact path:
  `C:\Users\HP\OneDrive\Documents\Playground\artifacts\anterior\anterior_uveitis_vs_normal_v1_simplecnn`
- packaged handoff path:
  `C:\Users\HP\OneDrive\Documents\Playground\handoff\macbook_next_specialist_packages\anterior_uveitis_vs_normal_v1_simplecnn_package`
- label map:
  `normal -> 0`, `uveitis -> 1`
- preprocessing contract:
  RGB, `224 x 224`, direct resize, `float32`, model contains internal
  `Rescaling(1.0 / 255.0)`
- threshold strategy:
  threshold-tuned binary decision on the `uveitis` score with
  `selected_threshold=0.5`
- validation metrics:
  best checkpoint `val_accuracy=0.9792`, `val_loss=0.1344`
  threshold-tuned `balanced_accuracy=0.9846`
- test metrics:
  default `test_accuracy=0.9846`
  default confusion matrix `[[96, 1], [1, 32]]`
  threshold-tuned `test_accuracy=0.9846`
  threshold-tuned confusion matrix `[[96, 1], [1, 32]]`
- deployment status:
  `evaluation_only`
- app integration status:
  integrated on the Mac in `anterior_screening_eval_v4`
- intended use:
  optional follow-on specialist after `surface_abnormal` to narrow some
  inflammatory-looking cases
- known failure modes:
  single-source bootstrap only, no external holdout, and likely overlap with
  other red-eye causes

### `anterior_pterygium_vs_normal_v1_simplecnn`

- exact dataset path:
  `F:\datasets\Image Dataset on Eye Diseases Classification.zip`
- exact manifest path:
  `C:\Users\HP\OneDrive\Documents\Playground\datasets\manifests\anterior_pterygium_vs_normal_v1.jsonl`
- exact config path:
  `C:\Users\HP\OneDrive\Documents\Playground\configs\anterior_pterygium_vs_normal_v1_simplecnn.json`
- exact artifact path:
  `C:\Users\HP\OneDrive\Documents\Playground\artifacts\anterior\anterior_pterygium_vs_normal_v1_simplecnn`
- packaged handoff path:
  `C:\Users\HP\OneDrive\Documents\Playground\handoff\macbook_next_specialist_packages\anterior_pterygium_vs_normal_v1_simplecnn_package`
- label map:
  `normal -> 0`, `pterygium -> 1`
- preprocessing contract:
  RGB, `224 x 224`, direct resize, `float32`, model contains internal
  `Rescaling(1.0 / 255.0)`
- threshold strategy:
  threshold-tuned binary decision on the `pterygium` score with
  `selected_threshold=0.05`
- validation metrics:
  best checkpoint `val_accuracy=1.0000`, `val_loss=0.0262`
  threshold-tuned `balanced_accuracy=1.0000`
- test metrics:
  default `test_accuracy=1.0000`
  default confusion matrix `[[97, 0], [0, 15]]`
  threshold-tuned `test_accuracy=1.0000`
  threshold-tuned confusion matrix `[[97, 0], [0, 15]]`
- deployment status:
  `evaluation_only`
- app integration status:
  integrated on the Mac in `anterior_screening_eval_v4`
- intended use:
  optional follow-on specialist after `surface_abnormal` for a more specific
  evaluation-only label such as `Possible pterygium pattern detected`
- known failure modes:
  current local support is tiny with only `72` positive train images and `15`
  positive test images, so the perfect score should be treated cautiously

### `anterior_eyelid_abnormality_vs_normal_v1_simplecnn`

- exact dataset path:
  `F:\datasets\Image Dataset on Eye Diseases Classification.zip`
- exact manifest path:
  `C:\Users\HP\OneDrive\Documents\Playground\datasets\manifests\anterior_eyelid_abnormality_vs_normal_v1.jsonl`
- exact config path:
  `C:\Users\HP\OneDrive\Documents\Playground\configs\anterior_eyelid_abnormality_vs_normal_v1_simplecnn.json`
- exact artifact path:
  `C:\Users\HP\OneDrive\Documents\Playground\artifacts\anterior\anterior_eyelid_abnormality_vs_normal_v1_simplecnn`
- packaged handoff path:
  `C:\Users\HP\OneDrive\Documents\Playground\handoff\macbook_next_specialist_packages\anterior_eyelid_abnormality_vs_normal_v1_simplecnn_package`
- label map:
  `eyelid_abnormality -> 0`, `normal -> 1`
- preprocessing contract:
  RGB, `224 x 224`, direct resize, `float32`, model contains internal
  `Rescaling(1.0 / 255.0)`
- threshold strategy:
  threshold-tuned binary decision on the `eyelid_abnormality` score with
  `selected_threshold=0.35`
- validation metrics:
  best checkpoint `val_accuracy=0.9205`, `val_loss=0.2539`
  threshold-tuned `balanced_accuracy=0.9247`
- test metrics:
  default `test_accuracy=0.9318`
  default confusion matrix `[[72, 7], [5, 92]]`
  threshold-tuned `test_accuracy=0.9261`
  threshold-tuned confusion matrix `[[74, 5], [8, 89]]`
- deployment status:
  `evaluation_only`
- app integration status:
  not integrated; optional-use only
- intended use:
  optional separate specialist only if eyelid findings remain in product scope
- known failure modes:
  not a clean surface-only head, depends on eyelid visibility in framing, and
  the selected validation threshold generalized slightly worse than plain
  `argmax` on the held-out local test split

## Best next Mac review order

1. compare `anterior_quality_gate_v2_teyeds_simplecnn` against the current
   `anterior_quality_gate_v1` on real app captures before changing the front
   gate
2. keep the current integrated six-stage anterior pipeline stable behind that
   quality-gate review
3. externally validate the integrated `uveitis` branch on broader holdout data
4. externally validate the integrated `pterygium` branch and keep it
   explicitly cautious because of tiny local support
5. only pull `anterior_eyelid_abnormality_vs_normal_v1_simplecnn` into the app
   if eyelid findings are intentionally in scope

## Current local fundus baseline note

### `fundus_router_v1_simplecnn`

- exact artifact path:
  `C:\Users\HP\OneDrive\Documents\Playground\artifacts\router\fundus_router_v1_simplecnn`
- test metrics:
  `test_accuracy=0.9819`
  confusion matrix `[[343, 17], [4, 794]]`
- deployment status:
  `evaluation_only`
- intended use:
  image-type routing between anterior and fundus inputs

### `fundus_dr_vs_healthy_v1_simplecnn`

- exact artifact path:
  `C:\Users\HP\OneDrive\Documents\Playground\artifacts\fundus\fundus_dr_vs_healthy_v1_simplecnn`
- test metrics:
  `test_accuracy=0.7842`
  threshold-tuned `balanced_accuracy=0.7652`
- deployment status:
  `evaluation_only`
- intended use:
  local fundus DR baseline only, not yet strong enough for integration

### `fundus_glaucoma_vs_healthy_v1_simplecnn`

- exact artifact path:
  `C:\Users\HP\OneDrive\Documents\Playground\artifacts\fundus\fundus_glaucoma_vs_healthy_v1_simplecnn`
- test metrics:
  `test_accuracy=0.6798`
  threshold-tuned `balanced_accuracy=0.7001`
- deployment status:
  `evaluation_only`
- intended use:
  local glaucoma baseline only, not integration-ready

## Rejected fundus reruns from this pass

- `fundus_glaucoma_vs_healthy_v2_balanced_simplecnn`
  matched the weak `v1` baseline instead of improving it
- `fundus_dr_vs_healthy_v2_balanced_simplecnn`
  finished slightly worse than `v1`
- `fundus_glaucoma_vs_healthy_v3_mobilenet`
  performed materially worse with `test_accuracy=0.5674`
- `fundus_glaucoma_vs_healthy_v4_mobilenet_headonly`
  also collapsed to the disease class with `test_accuracy=0.5674` and
  confusion matrix `[[202, 0], [154, 0]]`
- `fundus_dr_vs_healthy_v3_mobilenet_headonly`
  also collapsed to the disease class with `test_accuracy=0.5947` and
  confusion matrix `[[226, 0], [154, 0]]`

## Deprioritized for this pass

- glaucoma-specific work is parked unless it is already mid-run
- fundus artifacts still exist locally, but the current app-facing priority is
  better specificity for anterior surface-positive results
- no new local fundus disease specialist is recommended for Mac integration
  from this pass; the next likely fundus gain needs better specialist data
  rather than another small local rerun

## Prepared but not yet trained external fundus runs

- `fundus_dr_idrid_v1_simplecnn`
  manifest path:
  `C:\Users\HP\OneDrive\Documents\Playground\datasets\manifests\fundus_dr_idrid_v1.jsonl`
  config path:
  `C:\Users\HP\OneDrive\Documents\Playground\configs\fundus_dr_idrid_v1_simplecnn.json`
  expected dataset path:
  `F:\datasets\External Fundus\IDRiD_DR_vs_Healthy`
  deployment status:
  `pending_dataset`
- `fundus_glaucoma_refuge_v1_simplecnn`
  manifest path:
  `C:\Users\HP\OneDrive\Documents\Playground\datasets\manifests\fundus_glaucoma_refuge_v1.jsonl`
  config path:
  `C:\Users\HP\OneDrive\Documents\Playground\configs\fundus_glaucoma_refuge_v1_simplecnn.json`
  expected dataset path:
  `F:\datasets\External Fundus\REFUGE_Glaucoma_vs_Healthy`
  deployment status:
  `pending_dataset`
- `fundus_glaucoma_papila_v1_simplecnn`
  manifest path:
  `C:\Users\HP\OneDrive\Documents\Playground\datasets\manifests\fundus_glaucoma_papila_v1.jsonl`
  config path:
  `C:\Users\HP\OneDrive\Documents\Playground\configs\fundus_glaucoma_papila_v1_simplecnn.json`
  expected dataset path:
  `F:\datasets\External Fundus\PAPILA_Glaucoma_vs_Healthy`
  deployment status:
  `pending_dataset`

## Foundation-model prep status

- checker path:
  `C:\Users\HP\OneDrive\Documents\Playground\Eye-Scan-App-Shared---Handoff\scripts\check_foundation_model_staging.py`
- latest verifier result:
  `0 / 4` staged weight files present
- exact blocker:
  `F:\datasets\FoundationModels` does not exist yet
- current status:
  `pending_download`
- note:
  no VisionFM or RETFound transfer-learning artifact exists yet in this lane
  because the required official weights are still missing

## External fundus inspection status

### `Eye-Fundus.zip`

- exact dataset path:
  `F:\Datasets\External Fundus\Eye-Fundus.zip`
- inspected structure:
  zip-backed `train`, `valid`, and `test` class folders
- inspected scale:
  `16,242` images across `10` labels
- sample image size:
  `224 x 224`
- status:
  `usable_fallback_dataset`
- recommended future use:
  fallback `diabetic_retinopathy_vs_healthy` and `glaucoma_vs_healthy`
  experiments if better official fundus data is still unavailable
- known failure modes:
  rehosted provenance, pre-resized images, and trailing spaces in some label
  folder names inside the zip

### `RFMiD2_0.zip`

- exact dataset path:
  `F:\Datasets\External Fundus\RFMiD2_0.zip`
- inspected structure:
  outer archive contains `Training_set.zip`, `Validation_set.zip`, and
  `Test_set.zip`
- inspected image counts:
  train `509`, val `177`, test `174`
- sample image size:
  `512 x 512`
- status:
  `incomplete_download`
- blocker:
  no label CSV or annotation file was present in the downloaded archive, so
  the current file alone is not trainable

### `1. Original Images.zip`

- exact dataset path:
  `F:\Datasets\External Fundus\1. Original Images.zip`
- inspected structure:
  `3,200` PNG images under `a. Training Set`, `b. Validation Set`, and
  `c. Testing Set`
- inspected split counts:
  train `1,920`, val `640`, test `640`
- sample image size:
  `2144 x 1424`
- status:
  `trainable_multilabel_package`
- recommended future use:
  fundus multi-label screening experiments and derived binary fundus tasks once
  the training recipe for this package is chosen
- matching label files:
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
- status:
  `separate_armd_archive`
- known failure modes:
  not the missing RFMiD annotation package and not a broad multi-disease label
  file
