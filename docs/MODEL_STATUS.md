# Model Status

Last updated: 2026-03-23 21:36 AEDT

## Current integrated anterior app pipeline

1. `eye_vs_non_eye_gate_v1_simplecnn`
2. `anterior_quality_gate_v1`
3. `anterior_surface_binary_v2_simplecnn`
4. `anterior_conjunctivitis_vs_normal_v1_simplecnn` only after `surface_abnormal`
5. `anterior_uveitis_vs_normal_v1_simplecnn` only after `surface_abnormal`
   and only when conjunctivitis stays negative
6. `anterior_pterygium_vs_normal_v1_simplecnn` only after `surface_abnormal`
   and only when both conjunctivitis and uveitis stay negative
7. `anterior_cataract_vs_normal_v1_simplecnn` only after `normal_surface`

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

### `eye_vs_non_eye_gate_v1_simplecnn`

- exact dataset path:
  `F:\datasets\Image Dataset on Eye Diseases Classification.zip` plus sampled
  non-eye images from the `2017` through `2025`, `Google Photos`, and
  `Old Pics` folders on the F drive
- exact manifest path:
  `C:\Users\HP\OneDrive\Documents\Playground\datasets\manifests\eye_vs_non_eye_v1.jsonl`
- exact config path:
  `C:\Users\HP\OneDrive\Documents\Playground\configs\eye_vs_non_eye_gate_v1_simplecnn.json`
- exact artifact path:
  `C:\Users\HP\OneDrive\Documents\Playground\artifacts\router\eye_vs_non_eye_gate_v1_simplecnn`
- packaged handoff path:
  `C:\Users\HP\OneDrive\Documents\Playground\handoff\macbook_eye_presence_packages\eye_vs_non_eye_gate_v1_simplecnn_package`
- F-drive package copy:
  `F:\EyeScan App\Datasets\eye_vs_non_eye_gate_v1_simplecnn_package.zip`
- label map:
  `eye -> 0`, `non_eye -> 1`
- preprocessing contract:
  RGB, `224 x 224`, direct resize, `float32`, model contains internal
  `Rescaling(1.0 / 255.0)`
- threshold strategy:
  threshold-tuned binary decision on the `eye` score with
  `selected_threshold=0.35`
- validation metrics:
  threshold-tuned `val_accuracy=0.9858`
  threshold-tuned `balanced_accuracy=0.9856`
- test metrics:
  default `test_accuracy=0.9830`
  default confusion matrix `[[354, 6], [6, 339]]`
  threshold-tuned `test_accuracy=0.9844`
  threshold-tuned confusion matrix `[[358, 2], [9, 336]]`
- deployment status:
  `evaluation_only`
- intended use:
  pre-pipeline blocker model to keep obvious non-eye images from entering the
  EyeScan anterior pipeline
- Mac integration status:
  integrated ahead of `anterior_quality_gate_v1` in the local backend as of
  `anterior_screening_eval_v7`
- known failure modes:
  non-eye negatives come from weakly curated personal-photo folders rather than
  a dedicated benchmark, and the final checkpoint evaluation excluded one
  corrupt JPEG from the test split

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

## External fundus specialist status

- `fundus_dr_idrid_v1_simplecnn`
  artifact path:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/artifacts/fundus/fundus_dr_idrid_v1_simplecnn`
  source dataset path:
  `/Users/bharatsharma/Desktop/Eye Scan App Handoff/Datasets 2026/External Fundus/IDRiD_DR_vs_Healthy`
  local split counts:
  train `241` diabetic retinopathy / `125` healthy, val `57` diabetic
  retinopathy / `18` healthy, test `50` diabetic retinopathy / `25` healthy
  test result:
  tuned-threshold accuracy `0.7733`, balanced accuracy `0.7900`,
  threshold `0.75`
  current status:
  `strong_local_baseline_superseded_by_v3`
- `fundus_dr_idrid_v2_efficientnetb0_colab`
  training route:
  self-contained Colab notebook
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/Google Colab/Fundus DR IDRiD/fundus_dr_idrid_v2_efficientnetb0_colab.ipynb`
  output directory:
  `MyDrive/EyeScan_Models/Fundus_DR_IDRiD_V2`
  downloaded model zip:
  `/Users/bharatsharma/Desktop/Eye Scan App Handoff/Models 2026/Fundus_DR_IDRiD_V2-20260326T034353Z-3-001.zip`
  extracted artifact path:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/artifacts/fundus/fundus_dr_idrid_v2_efficientnetb0_colab_download/Fundus_DR_IDRiD_V2`
  reported device:
  `1` GPU visible in Colab
  preserved official split counts:
  train `226` diabetic retinopathy / `110` healthy, valid `53` diabetic
  retinopathy / `24` healthy, test `69` diabetic retinopathy / `34` healthy
  validation result:
  selected threshold `0.5`, balanced accuracy `0.8015`
  test result at default/tuned threshold:
  accuracy `0.7670`, balanced accuracy `0.7440`
  confusion matrix:
  `[[23, 11], [13, 56]]`
  current status:
  `completed_candidate_not_promoted`
- `fundus_dr_idrid_v3_efficientnetb2_balanced_colab`
  training route:
  self-contained Colab notebook
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/Google Colab/Fundus DR IDRiD/fundus_dr_idrid_v3_efficientnetb2_balanced_colab.ipynb`
  output directory:
  `MyDrive/EyeScan_Models/Fundus_DR_IDRiD_V3`
  downloaded model zip:
  `/Users/bharatsharma/Desktop/Eye Scan App Handoff/Models 2026/Fundus_DR_IDRiD_V3-20260326T051514Z-3-001.zip`
  extracted artifact path:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/artifacts/fundus/fundus_dr_idrid_v3_efficientnetb2_balanced_colab_download/Fundus_DR_IDRiD_V3`
  package zip:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/packages/fundus_dr_idrid_v3_efficientnetb2_balanced_colab_package.zip`
  reported device:
  `1` GPU visible in Colab
  preserved official split counts:
  train `226` diabetic retinopathy / `110` healthy, valid `53` diabetic
  retinopathy / `24` healthy, test `69` diabetic retinopathy / `34` healthy
  training recipe note:
  `EfficientNetB2`, `260 x 260`, balanced `50 / 50` sampler, staged deeper
  fine-tuning, `resize_with_pad`
  validation result:
  selected threshold `0.5`, balanced accuracy `0.9017`
  test result at default/tuned threshold:
  accuracy `0.7961`, balanced accuracy `0.8105`
  confusion matrix:
  `[[29, 5], [16, 53]]`
  current status:
  `preferred_current_idrid_candidate`
- note:
  the stronger GPU `EfficientNetB2` `IDRiD` rerun now beats both the earlier
  local `fundus_dr_idrid_v1_simplecnn` baseline (`0.7733` / `0.7900`) and the
  earlier Colab `v2` run (`0.7670` / `0.7440`), so `v3` is now the preferred
  current `IDRiD` diabetic-retinopathy specialist candidate
- `fundus_glaucoma_refuge_v1_simplecnn`
  manifest path:
  `C:\Users\HP\OneDrive\Documents\Playground\datasets\manifests\fundus_glaucoma_refuge_v1.jsonl`
  config path:
  `C:\Users\HP\OneDrive\Documents\Playground\configs\fundus_glaucoma_refuge_v1_simplecnn.json`
  expected dataset path:
  `F:\datasets\External Fundus\REFUGE_Glaucoma_vs_Healthy`
  current note:
  REFUGE download is still access-gated, so no Mac/Desktop staging folder exists
  yet for this run
  deployment status:
  `pending_dataset`
- `fundus_glaucoma_rimone_v1_vgg19_byhospital_colab`
  source type:
  official public fallback glaucoma comparison dataset
  current Colab bundle:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/Google Colab/Fundus Glaucoma RIM-ONE DL/fundus_glaucoma_rimone_v1_vgg19_byhospital_colab.ipynb`
  bundle note:
  stronger GPU path now prepared using the official `RIM-ONE DL` repository
  image download link; defaults to the harder official `by_hospital` split and
  uses a `VGG19` transfer-learning recipe aligned with the published benchmark
  latest Colab run:
  `fundus_glaucoma_rimone_v1_vgg19_byhospital_colab`
  output path:
  `MyDrive/EyeScan_Models/Fundus_Glaucoma_RIM_ONE_DL_V1`
  extracted count summary:
  train `160` healthy / `95` glaucoma, valid `35` healthy / `21` glaucoma,
  test `118` healthy / `56` glaucoma
  archive/layout note:
  the official zip contained both official split variants; the script matched
  `485` images from the `by_hospital` variant and ignored the equally-sized
  random variant paths as intended
  validation result:
  selected threshold `0.35`, balanced accuracy `0.7333`
  test result at default threshold:
  accuracy `0.7069`, balanced accuracy `0.5775`
  confusion matrix:
  `[[111, 7], [44, 12]]`
  test result at tuned threshold:
  accuracy `0.6954`, balanced accuracy `0.5972`
  confusion matrix:
  `[[103, 15], [38, 18]]`
  comparison note:
  this first `RIM-ONE DL` pass completed cleanly and confirms the direct
  official-download workflow works, but the model underperforms both the current
  `Eye-Fundus` fallback glaucoma artifact and the official `RIM-ONE DL`
  published `VGG19` by-hospital benchmark, so do not promote or package it
  deployment status:
  `completed_underperforming_comparison`
- `fundus_glaucoma_chaksu_v1_efficientnetb2_colab`
  source type:
  official public glaucoma-specific comparison dataset
  current Colab bundle:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/Google Colab/Fundus Glaucoma Chaksu/fundus_glaucoma_chaksu_v1_efficientnetb2_colab.ipynb`
  bundle note:
  stronger GPU path now prepared using the official public Figshare archive,
  the official train/test split, and the glaucoma-decision tables to reconstruct
  a binary healthy-vs-glaucoma image-only recipe
  correction note:
  Nature published an author correction on `2023-04-06`; current assumption is
  that it does not alter the image labels or train/test split semantics used by
  this bundle
  deployment status:
  `prepared_not_run`
- `fundus_glaucoma_papila_v1_simplecnn`
  manifest path:
  `C:\Users\HP\OneDrive\Documents\Playground\datasets\manifests\fundus_glaucoma_papila_v1.jsonl`
  config path:
  `C:\Users\HP\OneDrive\Documents\Playground\configs\fundus_glaucoma_papila_v1_simplecnn.json`
  expected dataset path:
  `F:\datasets\External Fundus\PAPILA_Glaucoma_vs_Healthy`
  current Mac/Desktop staging path:
  `/Users/bharatsharma/Desktop/Eye Scan App Handoff/Datasets 2026/External Fundus/PAPILA_Glaucoma_vs_Healthy`
  current staged counts:
  `87` glaucoma, `333` healthy, `68` suspicious excluded
  current Colab bundle:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/Google Colab/Fundus Glaucoma PAPILA/fundus_glaucoma_papila_v3_efficientnetb2_officialfold_colab.ipynb`
  bundle note:
  stronger GPU path now prepared using either the raw `PAPILA.zip` archive on
  Google Drive or a direct public Figshare download, plus the official
  `HelpCode/kfold/Test 2` binary fold files while keeping full-image
  preprocessing for future backend compatibility
  correction note:
  Nature published an author correction on `2024-04-17`; current assumption is
  that it does not alter the binary image labels or official fold semantics
  latest Colab run:
  `fundus_glaucoma_papila_v3_efficientnetb2_officialfold_colab`
  output path:
  `MyDrive/EyeScan_Models/Fundus_Glaucoma_PAPILA_V3`
  official fold summary:
  train fold rows `336`, test fold rows `84`, diagnosis mismatches `0`
  validation result:
  selected threshold `0.35`, balanced accuracy `0.7759`
  test result at default threshold:
  accuracy `0.8214`, balanced accuracy `0.7170`
  confusion matrix:
  `[[59, 6], [9, 10]]`
  test result at tuned threshold:
  accuracy `0.8333`, balanced accuracy `0.7619`
  confusion matrix:
  `[[58, 7], [7, 12]]`
  comparison note:
  this is a real improvement over the earlier weak local PAPILA baseline, but
  it still does not clearly beat the current `Eye-Fundus` fallback glaucoma
  model on balanced accuracy (`0.7730` tuned on a larger held-out test set), so
  keep it as an evaluation/comparison candidate rather than the promoted
  default glaucoma specialist for now
  deployment status:
  `completed_comparison_candidate`

## Mac `Eye-Fundus` fallback glaucoma runs

- `fundus_glaucoma_eyefundus_v1_simplecnn`
  artifact path:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/artifacts/fundus/fundus_glaucoma_eyefundus_v1_simplecnn`
  extracted dataset root:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/datasets/fundus/Eye_Fundus_Glaucoma_vs_Healthy`
  preserved split counts:
  train `2015` glaucoma / `1873` healthy, val `576` glaucoma / `535` healthy,
  test `289` glaucoma / `268` healthy
  test result:
  tuned-threshold accuracy `0.6373`, balanced accuracy `0.6363`,
  threshold `0.55`
  current status:
  `fallback_local_only`
- `fundus_glaucoma_eyefundus_v2_augmented_simplecnn`
  artifact path:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/artifacts/fundus/fundus_glaucoma_eyefundus_v2_augmented_simplecnn`
  test result:
  default/tuned accuracy `0.6140`, balanced accuracy `0.6154`
  current status:
  `rejected_local_rerun`
- recommendation:
  keep `fundus_glaucoma_eyefundus_v1_simplecnn` only as a temporary CPU-side
  fallback artifact; it is better than the PAPILA local baseline, but no
  longer the strongest `Eye-Fundus` glaucoma run

## Colab `Eye-Fundus` fallback glaucoma run

- `fundus_glaucoma_eyefundus_v3_efficientnetb0_colab`
  training route:
  self-contained Colab notebook
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/Google Colab/Fundus Glaucoma Fallback/fundus_glaucoma_eyefundus_v3_efficientnetb0_colab.ipynb`
  dataset source:
  `MyDrive/Datasets/eye_fundus_glaucoma_vs_healthy.zip`
  output directory:
  `MyDrive/EyeScan_Models/Fundus_Glaucoma_EyeFundus_V3`
  reported device:
  `1` GPU visible in Colab
  preserved split counts:
  train `2015` glaucoma / `1873` healthy, val `576` glaucoma / `535` healthy,
  test `289` glaucoma / `268` healthy
  validation result:
  selected threshold `0.4`, balanced accuracy `0.8052`
  test result at default threshold:
  accuracy `0.7684`, balanced accuracy `0.7722`
  test result at tuned threshold:
  accuracy `0.7720`, balanced accuracy `0.7730`
  confusion matrix at tuned threshold:
  `[[214, 54], [73, 216]]`
  current status:
  `preferred_fallback_candidate`
- note:
  this is currently the strongest completed glaucoma fallback artifact from the
  `Eye-Fundus` lane and clearly outperforms the Mac CPU baselines; however, it
  is still a fallback path rather than the final preferred specialist-data
  solution

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

## Colab anterior view router run

- `anterior_view_router_v1_mobilenetv2_binary_colab_20260330_125330`
  training route:
  self-contained Colab notebook
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/Google Colab/Anterior View Router/train_anterior_view_router_v1_binary_colab.ipynb`
  companion training script:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/Google Colab/Anterior View Router/train_anterior_view_router_v1_binary_colab.py`
  dataset source:
  `MyDrive/Datasets/anterior_view_router_v1_binary_colab_dataset.zip`
  output directory:
  `MyDrive/EyeScan_Models/Anterior_View_Router_V1_Binary/runs/anterior_view_router_v1_mobilenetv2_binary_colab_20260330_125330`
  downloaded Desktop export:
  `/Users/bharatsharma/Desktop/Eye Scan App Handoff/Models 2026/anterior_view_router_v1_mobilenetv2_binary_colab_20260330_125330_package.zip`
  package zip staged in shared repo:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/packages/anterior_view_router_v1_mobilenetv2_binary_colab_20260330_125330_package.zip`
  extracted artifact path:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/artifacts/anterior/anterior_view_router_v1_mobilenetv2_binary_colab_download/anterior_view_router_v1_mobilenetv2_binary_colab_20260330_125330_package`
  class map:
  `eyelid_dominant -> 0`, `iris_visible -> 1`
  preserved split counts:
  train `175` eyelid_dominant / `1247` iris_visible, val `31` eyelid_dominant /
  `268` iris_visible, test `37` eyelid_dominant / `284` iris_visible
  balancing strategy:
  `class_weight`, eyelid_dominant `4.0629`, iris_visible `0.5702`
  validation result:
  accuracy `0.9398`, AUC `0.9784`, precision `0.9771`, recall `0.9552`
  test result:
  accuracy `0.9502`, AUC `0.9717`
  eyelid_dominant test result:
  precision `0.7838`, recall `0.7838`, F1 `0.7838`
  confusion matrix:
  `[[29, 8], [8, 276]]`
  runtime fallback contract:
  if `p(iris_visible) >= 0.65` route `iris_visible`; if `p(iris_visible) <= 0.35`
  route `eyelid_dominant`; otherwise return `low_confidence_fallback`
  offline quick-check note:
  a local 24-image sample audit against the reviewed source dataset routed
  `12 / 12` iris_visible samples correctly and `11 / 12` eyelid_dominant
  samples correctly, with the remaining eyelid case falling into the intended
  low-confidence fallback instead of a bad hard route
  deployment status:
  `completed_offline_candidate_not_integrated`
  current recommendation:
  keep this as the preferred trained anterior view-router candidate for offline
  validation and local backend staging, but do not switch the live app/backend
  off the current heuristic router until a small real-photo regression pass is
  completed
