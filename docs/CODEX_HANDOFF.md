# EyeScan Codex Handoff

Last updated: 2026-03-23 02:08 AEDT

## Shared goal

Keep EyeScan honest while moving the vague surface-positive branch toward more
specific evaluation-only outputs.

## What the Mac side already has

- integrated:
  - `anterior_quality_gate_v1`
  - `anterior_surface_binary_v2_simplecnn`
  - `anterior_conjunctivitis_vs_normal_v1_simplecnn`
  - `anterior_uveitis_vs_normal_v1_simplecnn`
  - `anterior_pterygium_vs_normal_v1_simplecnn`
  - `anterior_cataract_vs_normal_v1_simplecnn`
- live app can already show:
  - `Possible cataract pattern detected`
  - `Possible conjunctivitis pattern detected`
  - `Possible uveitis pattern detected`
  - `Possible pterygium pattern detected`
  - `Surface abnormality pattern detected`
  - `No screen-positive finding`
  - `Image quality needs recapture`

## What the Dell side added in this pass

- finished the remaining local surface-specialist training runs:
  - `anterior_uveitis_vs_normal_v1_simplecnn`
  - `anterior_pterygium_vs_normal_v1_simplecnn`
  - `anterior_eyelid_abnormality_vs_normal_v1_simplecnn`
- trained and packaged a new Dell-side quality-gate candidate:
  - `anterior_quality_gate_v2_teyeds_simplecnn`
- packaged Mac-ready artifact folders for those runs under:
  `C:\Users\HP\OneDrive\Documents\Playground\handoff\macbook_next_specialist_packages`
- refreshed the workspace and shared handoff docs with the new metrics and
  deployment recommendations

## Latest Mac integration note

- `anterior_uveitis_vs_normal_v1_simplecnn` is now integrated after
  conjunctivitis in the `surface_abnormal` branch
- `anterior_pterygium_vs_normal_v1_simplecnn` is now integrated after both
  conjunctivitis and uveitis stay negative
- live backend version is now:
  `anterior_screening_eval_v6`
- latest backend hardening:
  if `eye_detected == false`, specialist screening is blocked and the quality
  result falls back to `No clear eye detected`
- latest eye-feature hardening also adds a dark-band rejection check so laptop
  and screen captures are more likely to stop at `No clear eye detected`
  instead of leaking into a surface-positive specialist
- recent regression that triggered this fix:
  a laptop image was able to reach the screening pipeline under `eval_v4`
- `TEST_MODE` is now deliberately obvious across:
  - capture flow
  - result screen
  - single PDF export
  - multi-result PDF export
- the in-app yellow `TEST_MODE` banner text was darkened for readability on
  the dark theme
- PDF exports now use:
  - a centered `EyeScan / EYE HEALTH AI` text watermark
  - symbol-logo marks on both sides of the image row near the top
- branding assets were refreshed so:
  - the app icon uses the symbol-only EyeScan mark
  - the white launch screen uses the full `EyeScan / Eye Health AI` artwork

## Latest Mac monetization note

- Android Play Billing scaffold is now integrated into the Flutter app using
  `in_app_purchase`
- Android manifest now includes:
  `com.android.vending.BILLING`
- the app now has a clinic access screen plus settings and about-screen entry
  points
- default product IDs currently compiled into the app are:
  - subscription: `eyescan_plus`
- PDF gating for exports exists but currently defaults to off through:
  `EYESCAN_PREMIUM_GATING_ENABLED=false`
- recommended commercial model is now:
  `one clinic trial -> one clinic subscription`, not `one user -> one premium unlock`
- target trial design is:
  `14 days + 100 scans + up to 2 authorised users`
- latest billing-enabled Android bundle built on the Mac is:
  `1.1.6+15`
- current Play Console alignment note:
  the clinic-access strategy is mapped onto the existing live subscription
  product ID `eyescan_plus` so store testing can proceed without creating a
  second subscription
- practical next step is Play Console product setup plus backend clinic-trial
  enforcement design, not more Dell-side release/versioning work
- Android beta caveat:
  a release build uploaded without a reachable `EYESCAN_BACKEND_URL` falls
  back to `Image saved for later screening review` with `0%` quality and does
  not reach screening at all; future Play beta builds must either bake in a
  reachable backend URL or enable internal tools for tester-side backend entry

## New VisionFM pilot note

- a new ChatGPT-assisted VisionFM quality-gate pilot is ready for review
- reproducible notebook path on the Mac:
  `/Users/bharatsharma/Desktop/Google Console/Vision FM Files/VisionFM_Pilot.ipynb`
- treat it as a two-stage pipeline, not a single model:
  1. VisionFM backbone checkpoint `.pth`
  2. refined sklearn classifier `.pkl`
- provided Colab or Drive handoff paths:
  - `/content/drive/MyDrive/Datasets/VFM Datasets/VFM_External_weights.pth`
  - `/content/drive/MyDrive/EyeScan_Models/visionfm_quality_classifier_refined.pkl`
  - `/content/drive/MyDrive/EyeScan_Models/visionfm_quality_label_map_refined.json`
  - `/content/drive/MyDrive/EyeScan_Models/visionfm_quality_metadata_labeled.csv`
  - `/content/drive/MyDrive/EyeScan_Models/visionfm_quality_handoff_summary.json`
- refined classes are:
  - `bad`
  - `glare_lighting`
  - `good_centered`
  - `off_angle`
- strict instruction:
  use the refined label map only, ignore older non-refined quality artifacts,
  and do not integrate this into `erica_server.py` yet
- notebook flow confirmed:
  mount Drive, extract VisionFM embeddings from TEyeD images, cluster and
  inspect embeddings, relabel to `label_refined`, fit LogisticRegression, then
  export the refined classifier, refined label map, labeled metadata, and
  handoff summary
- shared-path caveat:
  this pilot does not yet replace the Dell-side `FoundationModels` staging
  requirement until the underlying `.pth` checkpoint is staged and verified in
  the expected shared location

## New VisionFM quality-gate training result

- a first Colab-based VisionFM external-eye linear-probe run is now complete
- exact notebook path in the shared repo:
  `Google Colab/Quality Gate/anterior_quality_gate_v3_visionfm_external_linearprobe.ipynb`
- exact Drive output folder:
  `/content/drive/MyDrive/EyeScan_Models/VisionFM_Quality_Gate_V3`
- exact backbone used:
  `/content/drive/MyDrive/Datasets/VFM Datasets/VFM_External_weights.pth`
- test summary:
  default `test_accuracy=0.9133`
  threshold-tuned `test_accuracy=0.9337`
  selected threshold `0.25` on `p(needs_recapture)`
  threshold-tuned confusion matrix `[[108, 13], [0, 75]]`
- deployment status:
  `evaluation_only`
- practical interpretation:
  promising first VisionFM transfer-learning candidate, but still a
  comparison/evaluation artifact rather than a live-gate replacement
- package paths for Mac inspection:
  - preferred slim handoff:
    `F:\EyeScan App\Datasets\VisionFM_Quality_Gate_V3_mac_handoff.zip`
  - full package if deeper inspection is needed:
    `F:\EyeScan App\Datasets\VisionFM_Quality_Gate_V3_package.zip`
- package note:
  the slim handoff keeps `best_model.pth` plus the contract JSON files and
  excludes the redundant `final_model.pth`

## New eye-vs-non-eye gate candidate

- a new pre-pipeline blocker candidate is now packaged from the Dell side:
  `eye_vs_non_eye_gate_v1_simplecnn`
- exact manifest path:
  `C:\Users\HP\OneDrive\Documents\Playground\datasets\manifests\eye_vs_non_eye_v1.jsonl`
- exact config path:
  `C:\Users\HP\OneDrive\Documents\Playground\configs\eye_vs_non_eye_gate_v1_simplecnn.json`
- exact artifact path:
  `C:\Users\HP\OneDrive\Documents\Playground\artifacts\router\eye_vs_non_eye_gate_v1_simplecnn`
- preferred packaged handoff path:
  `C:\Users\HP\OneDrive\Documents\Playground\handoff\macbook_eye_presence_packages\eye_vs_non_eye_gate_v1_simplecnn_package.zip`
- convenience copy on the F drive:
  `F:\EyeScan App\Datasets\eye_vs_non_eye_gate_v1_simplecnn_package.zip`
- test summary:
  default `test_accuracy=0.9830`
  threshold-tuned `test_accuracy=0.9844`
  selected threshold `0.35` on `p(eye)`
  threshold-tuned eye recall `0.9944`
  threshold-tuned non-eye recall `0.9739`
- deployment status:
  `evaluation_only`
- intended role:
  run before the current anterior quality gate so obvious non-eye images do not
  enter the rest of the pipeline
- important caveat:
  the non-eye class is sampled from personal-photo folders on the F drive, and
  one corrupt JPEG in the `2021 / Mercedes A170 accident` folder was removed
  from the test split before final checkpoint evaluation

## Coordination note

- be conservative with message budget in future model-training threads
- prefer short progress updates, a single source-of-truth doc update, and one
  consolidated handoff message instead of many small chat turns
- when ChatGPT/Colab is used for pilot training, always preserve:
  - the `.ipynb`
  - the checkpoint path
  - exported artifacts
  - one short handoff summary pointing at the canonical notebook

## New packaged quality-gate candidate

### `anterior_quality_gate_v2_teyeds_simplecnn`

- exact artifact path:
  `C:\Users\HP\OneDrive\Documents\Playground\artifacts\anterior\anterior_quality_gate_v2_teyeds_simplecnn`
- packaged handoff path:
  `C:\Users\HP\OneDrive\Documents\Playground\handoff\macbook_quality_gate_packages\anterior_quality_gate_v2_teyeds_simplecnn_package`
- threshold:
  `0.35` on `p(needs_recapture)`
- test summary:
  default `test_accuracy=0.8256`
  threshold-tuned `test_accuracy=0.8103`
  threshold-tuned confusion matrix `[[102, 18], [19, 56]]`
- deployment status:
  `evaluation_only`
- caution:
  useful as a real-data-backed review candidate, but not ready to replace the
  live gate until it is checked against actual EyeScan captures

## New packaged candidate artifacts

### `anterior_uveitis_vs_normal_v1_simplecnn`

- exact artifact path:
  `C:\Users\HP\OneDrive\Documents\Playground\artifacts\anterior\anterior_uveitis_vs_normal_v1_simplecnn`
- packaged handoff path:
  `C:\Users\HP\OneDrive\Documents\Playground\handoff\macbook_next_specialist_packages\anterior_uveitis_vs_normal_v1_simplecnn_package`
- threshold:
  `0.5` on `p(uveitis)`
- test summary:
  default `test_accuracy=0.9846`
  threshold-tuned `test_accuracy=0.9846`
  threshold-tuned confusion matrix `[[96, 1], [1, 32]]`
- deployment status:
  `evaluation_only`

### `anterior_pterygium_vs_normal_v1_simplecnn`

- exact artifact path:
  `C:\Users\HP\OneDrive\Documents\Playground\artifacts\anterior\anterior_pterygium_vs_normal_v1_simplecnn`
- packaged handoff path:
  `C:\Users\HP\OneDrive\Documents\Playground\handoff\macbook_next_specialist_packages\anterior_pterygium_vs_normal_v1_simplecnn_package`
- threshold:
  `0.05` on `p(pterygium)`
- test summary:
  default `test_accuracy=1.0000`
  threshold-tuned `test_accuracy=1.0000`
  threshold-tuned confusion matrix `[[97, 0], [0, 15]]`
- deployment status:
  `evaluation_only`
- caution:
  tiny local support makes this a high-variance result

### `anterior_eyelid_abnormality_vs_normal_v1_simplecnn`

- exact artifact path:
  `C:\Users\HP\OneDrive\Documents\Playground\artifacts\anterior\anterior_eyelid_abnormality_vs_normal_v1_simplecnn`
- packaged handoff path:
  `C:\Users\HP\OneDrive\Documents\Playground\handoff\macbook_next_specialist_packages\anterior_eyelid_abnormality_vs_normal_v1_simplecnn_package`
- threshold:
  `0.35` on `p(eyelid_abnormality)`
- test summary:
  default `test_accuracy=0.9318`
  threshold-tuned `test_accuracy=0.9261`
  threshold-tuned confusion matrix `[[74, 5], [8, 89]]`
- deployment status:
  `evaluation_only`
- caution:
  useful as an optional branch, but not a clean default replacement for the
  current surface-positive route

## Recommended next Mac sequence

1. keep the current integrated pipeline stable
2. externally validate the integrated `uveitis` and `pterygium` branches,
   especially the tiny-support `pterygium` head
3. keep monitoring the broad fallback rate for
   `Surface abnormality pattern detected`
4. compare `eye_vs_non_eye_gate_v1_simplecnn` against real false-entry cases
   like laptops, scenes, dashboards, and family photos before any app-side
   integration
5. only add `anterior_eyelid_abnormality_vs_normal_v1_simplecnn` if eyelid
   findings remain intentionally in scope
6. if no narrower specialist clears threshold, keep the fallback wording:
   `Surface abnormality pattern detected`

## Not the priority right now

- app release or version-code work from the Dell model lane
- glaucoma work unless it is already mid-run
- fundus cleanup ahead of the anterior surface-specificity gap

## Official foundation-model downloads now recommended

The next meaningful accuracy jump is more likely to come from official
ophthalmic pretrained backbones than from another small local rerun. The
current Dell recommendation is to stage these exact files on `F:\datasets`:

1. `F:\datasets\FoundationModels\VisionFM\ExternalEye\visionfm_external_eye.pth`
2. `F:\datasets\FoundationModels\VisionFM\SlitLamp\visionfm_slit_lamp.pth`
3. `F:\datasets\FoundationModels\RETFound\Fundus\retfound_dinov2_meh.pth`
4. `F:\datasets\FoundationModels\VisionFM\Fundus\visionfm_fundus.pth`

Prepared validator:

- `C:\Users\HP\OneDrive\Documents\Playground\scripts\check_foundation_model_staging.py`
- mirrored in the shared repo as:
  `scripts/check_foundation_model_staging.py`

Practical recommendation:

- start with `VisionFM External Eye` for the quality gate and surface-positive
  specialists because it is the closest modality match to the current app
- use `VisionFM Slit Lamp` as a secondary anterior comparison, not the first
  choice
- use `RETFound` and `VisionFM Fundus` only after the curated external fundus
  folders are staged

Current foundation-model state:

- the canonical `F:\datasets\FoundationModels` staging root still does not
  exist
- however, the actual downloaded files are now present in the alternate
  EyeScan dataset location:
  - `F:\Datasets\External Fundus\VFM Datasets\VFM_External_weights.pth`
  - `F:\Datasets\External Fundus\VFM Datasets\VFM_SiltLamp_weights.pth`
  - `F:\Datasets\External Fundus\VFM Datasets\RET Found Dino V2\RETFound_dinov2_meh.pth`
  - `F:\Datasets\External Fundus\VFM Datasets\VFM_Fundus_weights.pth`
- latest staging verification from the updated checker:
  `4 / 4` present
- current status:
  the foundation-model lane is no longer blocked on missing weights; the next
  honest work is notebook cleanup, real-capture comparison, and Mac-side
  review of the new VisionFM quality-gate package

## Latest fundus experiment note

- no new Mac-ready fundus package was promoted from this pass
- `fundus_glaucoma_vs_healthy_v2_balanced_simplecnn` was rejected because it
  did not improve over `v1`
- `fundus_dr_vs_healthy_v2_balanced_simplecnn` was rejected because it did not
  improve over `v1`
- `fundus_glaucoma_vs_healthy_v3_mobilenet` was rejected because it performed
  materially worse than the local baseline
- `fundus_glaucoma_vs_healthy_v4_mobilenet_headonly` was rejected because it
  collapsed to predicting `glaucoma` for every test image
- `fundus_dr_vs_healthy_v3_mobilenet_headonly` was rejected because it
  collapsed to predicting `diabetic_retinopathy` for every test image
- the best current local fundus-side artifact still remains
  `fundus_router_v1_simplecnn`
- practical recommendation:
  pause local fundus disease-specialist promotion until we have better
  specialist datasets or a more substantial recipe change

## Prepared next fundus path

- the Dell workspace now supports folder-backed manifests, not just zip-backed
  manifests
- verified by smoke test artifact:
  `C:\Users\HP\OneDrive\Documents\Playground\_scratch\artifacts\smoke_directory_manifest`
- prepared manifest tools:
  - `C:\Users\HP\OneDrive\Documents\Playground\scripts\build_directory_manifest.py`
  - `C:\Users\HP\OneDrive\Documents\Playground\scripts\prepare_external_manifests.py`
- prepared staged dataset roots:
  - `F:\datasets\External Fundus\IDRiD_DR_vs_Healthy`
  - `F:\datasets\External Fundus\REFUGE_Glaucoma_vs_Healthy`
  - `F:\datasets\External Fundus\PAPILA_Glaucoma_vs_Healthy`
- prepared next configs:
  - `C:\Users\HP\OneDrive\Documents\Playground\configs\fundus_dr_idrid_v1_simplecnn.json`
  - `C:\Users\HP\OneDrive\Documents\Playground\configs\fundus_glaucoma_refuge_v1_simplecnn.json`
  - `C:\Users\HP\OneDrive\Documents\Playground\configs\fundus_glaucoma_papila_v1_simplecnn.json`
- current blocker:
  the staged external fundus folders do not exist on `F:\datasets` yet, so
  these runs are `pending_dataset` rather than ready-to-train

## External fundus archive inspection note

- `F:\Datasets\External Fundus\Eye-Fundus.zip` is usable as a fallback local
  fundus source
- inspected structure:
  zip-backed `train`, `valid`, and `test` splits with class folders already
  encoded in the paths
- inspected scale:
  `16,242` images across `10` labels
- strongest immediate future uses:
  `diabetic_retinopathy_vs_healthy` and `glaucoma_vs_healthy`
- caveats:
  appears to be a rehosted single-label dataset, sample images are already
  `224 x 224`, and some label folder names inside the zip contain trailing
  spaces, so it is useful but not as clean as an official specialist source
- `F:\Datasets\External Fundus\RFMiD2_0.zip` is not yet trainable from the
  current download alone
- inspected structure:
  outer archive contains only `Training_set.zip`, `Validation_set.zip`, and
  `Test_set.zip`
- inspected image counts:
  train `509`, val `177`, test `174`
- blocker:
  no label CSV or annotation file was present in the downloaded archive, so a
  separate official label file or fuller package is still required
- `F:\Datasets\External Fundus\1. Original Images.zip` is now paired with the
  three RFMiD ground-truth CSVs and forms a complete trainable RFMiD package
- inspected structure:
  `3,200` PNG images under `a. Training Set`, `b. Validation Set`, and
  `c. Testing Set`
- inspected split counts:
  train `1,920`, val `640`, test `640`
- sample image size:
  `2144 x 1424`
- status:
  complete RFMiD image payload with matching labels
- matching ground-truth files:
  `a. RFMiD_Training_Labels.csv`, `b. RFMiD_Validation_Labels.csv`,
  `c. RFMiD_Testing_Labels.csv`
- label shape:
  `47` columns total with `45` disease label columns plus `Disease_Risk`
- `F:\Datasets\External Fundus\archive (1).zip` is not the missing RFMiD label
  package
- inspected structure:
  contains only `All ARMD images`
- inspected scale:
  `511` PNG images
- sample image size:
  `300 x 300`
- status:
  separate ARMD-only image archive, not the missing annotation bundle
