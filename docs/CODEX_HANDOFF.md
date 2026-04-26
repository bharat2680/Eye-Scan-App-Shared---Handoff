# EyeScan Codex Handoff

Last updated: 2026-04-03 23:34 AEDT

## Shared goal

Keep EyeScan honest while moving the vague surface-positive branch toward more
specific evaluation-only outputs.

## Current product priority

- prioritize anterior phone-capture reliability over more fundus breadth for
  now
- keep current fundus state as:
  `fundus_dr_idrid_v3_efficientnetb2_balanced_colab` for DR,
  `fundus_glaucoma_eyefundus_v3_efficientnetb0_colab` as the current fallback
  glaucoma specialist, and `fundus_glaucoma_chaksu_v1_efficientnetb2_colab` as
  the strongest provisional glaucoma comparison run
- pause further heavyweight fundus retraining until either the Chaksu
  preprocessing pipeline is improved or fundus becomes a near-term product
  priority again

## What the Mac side already has

- integrated:
  - `eye_vs_non_eye_gate_v1_simplecnn`
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

- current public Cloud Run revision is now:
  `eyescan-backend-beta-00006-pf6`
- live backend version is now:
  `anterior_screening_eval_v9`
- latest fundus hardening on the public backend:
  strong healthy fundus evidence can now override weaker glaucoma-only spikes,
  and glaucoma positives now require a higher confidence plus a healthier
  margin over the healthy signal before they are exported as positive
- practical expected public behavior now is:
  healthy or weak-confidence fundus images should fall back to
  `No clear disease pattern`, while only clearer glaucoma-like images should
  stay positive
- latest public verification pass on `2026-04-03` confirmed:
  non-eye images are blocked, anterior mode mismatch is blocked, and the
  public `/health` endpoint reports `anterior_screening_eval_v9`
- GitHub fine-grained token note:
  `EyeScan Shared Handoff Mac` exists for repo access, expires `2026-07-08`.
  Do not store the token value in this repo; keep it in Keychain or a
  password manager.

- Android/internal beta builds without a compiled backend URL no longer save
  misleading `0%` placeholder screening results as if they were real reviews
- those builds now expose the backend URL field in Settings even under release
  hardening, so testers can point the app at a real screening backend
- the missing-backend flow now sends the tester to Settings instead of creating
  fake saved results
- `eye_vs_non_eye_gate_v1_simplecnn` is now integrated as a pre-pipeline
  blocker ahead of the anterior quality gate
- the blocker is still `evaluation_only`, but it is now live in the Mac
  backend so obvious non-eye images can be stopped before they enter the
  screening router
- the blocker can also rescue some real-eye captures that the older heuristic
  detector would have rejected
- `anterior_uveitis_vs_normal_v1_simplecnn` is now integrated after
  conjunctivitis in the `surface_abnormal` branch
- `anterior_pterygium_vs_normal_v1_simplecnn` is now integrated after both
  conjunctivitis and uveitis stay negative
- latest backend hardening:
  if `eye_detected == false`, specialist screening is blocked and the quality
  result falls back to `No clear eye detected`
- latest eye-feature hardening also adds a dark-band rejection check so laptop
  and screen captures are more likely to stop at `No clear eye detected`
  instead of leaking into a surface-positive specialist
- recent regression that triggered this fix:
  a laptop image was able to reach the screening pipeline under `eval_v4`
- backend regression tests now explicitly cover:
  - eye-presence gate blocking a non-eye image before surface screening
  - eye-presence gate rescuing a real-eye image when the legacy heuristic is a
    false negative
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
- local backend is now also prepared for Google Cloud Run:
  - bundled quality model inside the backend runtime
  - Cloud Run Dockerfile added locally
  - Gunicorn + TensorFlow deployment dependencies added locally
  - Google Cloud auth, API enablement, and first beta deploy are now complete
- public backend is now live at:
  `https://eyescan-backend-beta-66791987039.australia-southeast2.run.app`
- Google Cloud beta host project is:
  `fine-elf-443312-d0`
- low-cost guardrail is now active:
  `EyeScan Beta Budget`
  `A$10/month`
  alerts at `50%`, `90%`, `100%`

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
  `1.1.7+17`
- current Android release state:
  production release `17 (1.1.7)` has been uploaded in Google Play Console and
  sent for review
- current Play Console alignment note:
  the clinic-access strategy is mapped onto the existing live subscription
  product ID `eyescan_plus` so store testing can proceed without creating a
  second subscription
- practical next step is complete Google Play review for production build
  `17 (1.1.7)`, verify purchase flow still matches `eyescan_plus`, and then
  move to backend clinic-trial enforcement design, not more Dell-side
  release/versioning work
- Android beta caveat:
  a release build uploaded without a reachable `EYESCAN_BACKEND_URL` falls
  back to `Image saved for later screening review` with `0%` quality and does
  not reach screening at all; future Play beta builds must either bake in a
  reachable backend URL or enable internal tools for tester-side backend entry
- current Mac-side fix:
  release-hardened builds now fall back to the public Cloud Run backend URL
  when no explicit backend URL is compiled in, so future beta bundles should
  no longer silently save local placeholder results

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
- Mac/Colab next-step bridge now prepared for PAPILA:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/Google Colab/Fundus Glaucoma PAPILA`
- prepared PAPILA Colab assets:
  `fundus_glaucoma_papila_v3_efficientnetb2_officialfold_colab.ipynb`
  and
  `train_fundus_glaucoma_papila_v3_officialfold_colab.py`
- PAPILA training recipe note:
  this path consumes the raw `PAPILA.zip` archive on Google Drive when present,
  but can also download the latest public Figshare `PAPILA` zip directly inside
  Colab; it rebuilds the official `HelpCode/kfold/Test 2` binary fold,
  preserves patient grouping for the held-out fold, and keeps full-image
  `resize_with_pad` preprocessing so a successful model stays closer to
  backend-deployable inference
- PAPILA correction note:
  the Scientific Data article now links an author correction published on
  `2024-04-17`; current working assumption is that this is not a binary-label or
  fold-definition change for the image-only training path
- PAPILA Colab run status:
  completed on Google Colab GPU and saved to
  `MyDrive/EyeScan_Models/Fundus_Glaucoma_PAPILA_V3`
- PAPILA metric snapshot:
  selected threshold `0.35`; validation balanced accuracy `0.7759`; tuned test
  accuracy `0.8333`; tuned test balanced accuracy `0.7619`
- PAPILA promotion decision:
  promising and materially better than the earlier local PAPILA attempt, but
  still not a clear enough win over the current `Eye-Fundus` fallback glaucoma
  artifact to replace it as the preferred current glaucoma model
- RIM-ONE DL next-step bundle prepared:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/Google Colab/Fundus Glaucoma RIM-ONE DL`
- prepared RIM-ONE assets:
  `fundus_glaucoma_rimone_v1_vgg19_byhospital_colab.ipynb`
  and
  `train_fundus_glaucoma_rimone_v1_vgg19_byhospital_colab.py`
- RIM-ONE recipe note:
  this path uses the official `RIM-ONE DL` repository download link for images
  when a Drive copy is not present, rebuilds a standard binary layout from the
  archive, and defaults to the official harder `by_hospital` split
- RIM-ONE model note:
  current first-pass recipe uses `VGG19` transfer learning because the official
  repository benchmark reports `VGG19` as a strong performer on both the random
  and by-hospital evaluations
- RIM-ONE Colab run status:
  completed on Google Colab GPU and saved to
  `MyDrive/EyeScan_Models/Fundus_Glaucoma_RIM_ONE_DL_V1`
- RIM-ONE metric snapshot:
  selected threshold `0.35`; validation balanced accuracy `0.7333`; tuned test
  accuracy `0.6954`; tuned test balanced accuracy `0.5972`
- RIM-ONE promotion decision:
  not good enough to promote; this first pass confirms the official download
  path and archive parsing work, but the model is materially weaker than both
  the current `Eye-Fundus` fallback glaucoma artifact and the official
  published `RIM-ONE DL` by-hospital `VGG19` benchmark
- Chaksu Colab run now completed on March 27, 2026:
  `fundus_glaucoma_chaksu_v1_efficientnetb2_colab`
- Chaksu Colab bundle path:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/Google Colab/Fundus Glaucoma Chaksu`
- Chaksu downloaded Desktop export:
  `/Users/bharatsharma/Desktop/Eye Scan App Handoff/Models 2026/Fundus_Glaucoma_Chaksu_V1-20260327T020932Z-3-001.zip`
- Chaksu local extraction path:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/artifacts/fundus/fundus_glaucoma_chaksu_v1_efficientnetb2_colab_download/Fundus_Glaucoma_Chaksu_V1`
- Chaksu result summary:
  selected threshold `0.6`; validation balanced accuracy `0.7337`;
  tuned-threshold test accuracy `0.7891`; tuned-threshold test balanced
  accuracy `0.8546`
- Chaksu coverage caveat:
  the successful run only staged a matched subset of the public archives
  (`193` train, `50` valid, `176` test) even though the raw split inspection
  saw `1014` train images and `631` test images; `metrics.json` still reports a
  large unmatched-image count
- Chaksu promotion decision:
  keep this as the strongest glaucoma comparison result collected so far, but
  do not immediately replace the current `Eye-Fundus` fallback glaucoma model
  in production because the dataset mapping is still incomplete and malformed
  image files were skipped to keep the run alive
- Chaksu next-step recommendation:
  do not spend more GPU time retraining the same pipeline; only revisit Chaksu
  after a cleaner `CPU prep -> GPU train` `v6` pipeline exists and the
  decision-table-to-image matching has been improved

## Pause fundus, focus anterior checklist

- `P0`: keep the current fundus lane stable and stop additional big fundus
  downloads for now
- `P1`: build a small real phone-capture anterior validation set from the app
- `P2`: label the phone captures into practical buckets:
  good, blur, glare, off-angle, too dark, too far or too close, and partial-eye
  or non-eye
- `P3`: compare the current anterior quality-gate candidates on that exact
  phone-capture set before training more disease heads
- `P4`: tune thresholds and recapture guidance around real phone captures, not
  just training-set behavior
- `P5`: improve capture UX copy in the app with direct prompts such as move
  closer, hold steady, avoid flash reflection, use brighter light, and open eye
  wider
- `P6`: keep the current anterior disease heads as-is for now and only retrain
  if the phone-capture evaluation shows a real weakness
- `P7`: revisit broader fundus work later only after anterior capture quality
  feels reliable in real user testing

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
- Mac local fallback glaucoma pass now completed:
  extracted dataset root
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/datasets/fundus/Eye_Fundus_Glaucoma_vs_Healthy`
- best fallback artifact from that pass:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/artifacts/fundus/fundus_glaucoma_eyefundus_v1_simplecnn`
- best fallback result:
  tuned-threshold accuracy `0.6373`, balanced accuracy `0.6363`
- second rerun note:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/artifacts/fundus/fundus_glaucoma_eyefundus_v2_augmented_simplecnn`
  underperformed the first run, so keep `v1` only as a temporary local
  fallback and do not promote it as the preferred long-term glaucoma
  specialist
- GPU next-step bundle prepared:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/Google Colab/Fundus Glaucoma Fallback`
  containing the Colab launcher notebook
  `fundus_glaucoma_eyefundus_v3_efficientnetb0_colab.ipynb`, training script
  `train_fundus_glaucoma_eyefundus_colab.py`, and compact upload-ready dataset
  `eye_fundus_glaucoma_vs_healthy.zip`
- Colab GPU run now completed on March 26, 2026:
  `fundus_glaucoma_eyefundus_v3_efficientnetb0_colab`
- reported Colab output directory:
  `MyDrive/EyeScan_Models/Fundus_Glaucoma_EyeFundus_V3`
- best reported test result:
  tuned-threshold accuracy `0.7720`, balanced accuracy `0.7730`,
  threshold `0.4`
- comparison note:
  this materially outperforms the prior Mac local fallback
  `fundus_glaucoma_eyefundus_v1_simplecnn` and is the current preferred
  `Eye-Fundus` glaucoma fallback candidate
- verification note:
  the result was recorded from the successful Colab console output; local
  Google Drive sync inspection was not available from this machine because the
  Drive path timed out during inspection
- backend-style package zip staged in shared repo:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/packages/fundus_glaucoma_eyefundus_v3_efficientnetb0_colab_package.zip`
  with `best_model.keras`, `metrics.json`, `label_map.json`,
  normalized `inference_contract.json`, `train_config.json`, and `HANDOFF.md`
- backend integration now added in:
  `/Users/bharatsharma/FlutterProjects/eye_scan_app/backend/app.py`
  and `/Users/bharatsharma/FlutterProjects/eye_scan_app/backend/Dockerfile`
- integration shape:
  `POST /v1/predict` now supports `requested_modality=fundus` and runs a
  multi-specialist fundus branch with:
  `fundus_dr_idrid_v3_efficientnetb2_balanced_colab` and
  `fundus_glaucoma_eyefundus_v3_efficientnetb0_colab`
- compatibility note:
  the exported Colab model required a one-key `.keras` sanitization
  (`quantization_config`) plus `compile=False` loading to run cleanly in the
  current backend runtime
- local verification:
  backend `/health` now reports both `fundus_dr_model_available: true` and
  `fundus_glaucoma_model_available: true`
- local prediction verification:
  a healthy `IDRiD` image returns `screen_negative` with both fundus
  specialists present, and a DR `IDRiD` image returns `screen_positive` with
  `Possible diabetic retinopathy` as the primary label while leaving the
  weaker glaucoma fallback hit visible in metadata
- next Colab training bundle prepared:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/Google Colab/Fundus DR IDRiD`
  with notebook `fundus_dr_idrid_v2_efficientnetb0_colab.ipynb`
- input expectation for that next run:
  upload raw `IDRiD` grading archive `B. Disease Grading.zip` to
  `MyDrive/Datasets/`
- storage note:
  this path avoids creating another local Mac copy of the `IDRiD` dataset and
  rebuilds the DR-vs-healthy splits directly in Colab
- Colab `IDRiD` run now completed on March 26, 2026:
  `fundus_dr_idrid_v2_efficientnetb0_colab`
- reported Colab output directory:
  `MyDrive/EyeScan_Models/Fundus_DR_IDRiD_V2`
- downloaded Desktop export:
  `/Users/bharatsharma/Desktop/Eye Scan App Handoff/Models 2026/Fundus_DR_IDRiD_V2-20260326T034353Z-3-001.zip`
- local extraction path:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/artifacts/fundus/fundus_dr_idrid_v2_efficientnetb0_colab_download/Fundus_DR_IDRiD_V2`
- verification note:
  the exported `.keras` file loads locally with `compile=False` and did not
  require the extra `quantization_config` sanitization that was needed for the
  glaucoma Colab export
- best reported validation result:
  selected threshold `0.5`, balanced accuracy `0.8015`
- best reported test result:
  accuracy `0.7670`, balanced accuracy `0.7440`, threshold `0.5`
- comparison note:
  this is a valid GPU-trained `IDRiD` export, but it currently underperforms
  the earlier local `fundus_dr_idrid_v1_simplecnn` baseline
  (`0.7733` accuracy / `0.7900` balanced accuracy), so keep the local `v1`
  run as the preferred current `IDRiD` candidate for now
- stronger `IDRiD` Colab rerun bundle now prepared:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/Google Colab/Fundus DR IDRiD/fundus_dr_idrid_v3_efficientnetb2_balanced_colab.ipynb`
- recipe changes for this stronger rerun:
  larger `EfficientNetB2` backbone, `260 x 260` input size, balanced
  `50 / 50` training sampler, longer staged fine-tuning, and
  `resize_with_pad` preprocessing
- target output directory for the stronger rerun:
  `MyDrive/EyeScan_Models/Fundus_DR_IDRiD_V3`
- stronger `IDRiD` rerun now completed on March 26, 2026:
  `fundus_dr_idrid_v3_efficientnetb2_balanced_colab`
- reported Colab output directory:
  `MyDrive/EyeScan_Models/Fundus_DR_IDRiD_V3`
- best reported validation result:
  selected threshold `0.5`, balanced accuracy `0.9017`
- best reported test result:
  accuracy `0.7961`, balanced accuracy `0.8105`, threshold `0.5`
- confusion matrix:
  `[[29, 5], [16, 53]]`
- promotion note:
  this stronger GPU `IDRiD` rerun now beats both the earlier local
  `fundus_dr_idrid_v1_simplecnn` baseline (`0.7733` / `0.7900`) and the
  earlier Colab `v2` run (`0.7670` / `0.7440`), so it becomes the preferred
  current `IDRiD` candidate
- downloaded Desktop export:
  `/Users/bharatsharma/Desktop/Eye Scan App Handoff/Models 2026/Fundus_DR_IDRiD_V3-20260326T051514Z-3-001.zip`
- local extraction path:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/artifacts/fundus/fundus_dr_idrid_v3_efficientnetb2_balanced_colab_download/Fundus_DR_IDRiD_V3`
- verification note:
  the exported `.keras` file also loads locally with `compile=False`
- backend-style package zip staged in shared repo:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/packages/fundus_dr_idrid_v3_efficientnetb2_balanced_colab_package.zip`
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

## March 31, 2026 update: anterior view router package completed offline

- completed Colab router run:
  `anterior_view_router_v1_mobilenetv2_binary_colab_20260330_125330`
- trainable label set:
  `eyelid_dominant`, `iris_visible`
- package zip preserved in shared repo:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/packages/anterior_view_router_v1_mobilenetv2_binary_colab_20260330_125330_package.zip`
- extracted artifact path:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/artifacts/anterior/anterior_view_router_v1_mobilenetv2_binary_colab_download/anterior_view_router_v1_mobilenetv2_binary_colab_20260330_125330_package`
- validation result:
  accuracy `0.9398`, AUC `0.9784`
- test result:
  accuracy `0.9502`, AUC `0.9717`
- eyelid-dominant class test result:
  precision `0.7838`, recall `0.7838`, F1 `0.7838`
- confusion matrix:
  `[[29, 8], [8, 276]]`
- runtime routing contract:
  iris route if `p(iris_visible) >= 0.65`, eyelid route if
  `p(iris_visible) <= 0.35`, else `low_confidence_fallback`
- local offline quick-check:
  `12 / 12` sampled iris_visible images routed correctly and
  `11 / 12` sampled eyelid_dominant images hard-routed correctly, with the
  remaining eyelid sample falling into the intended low-confidence fallback
- packaging cleanup:
  the Desktop export initially omitted `train_history.json` inside the zip; the
  shared package zip was rebuilt and now includes the full artifact set
- important current state:
  this router is staged offline only; the live backend still uses the current
  heuristic anterior view router (`anterior_view_rules_v1`) and has not been
  switched to this trained package yet
- dedicated review note:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/docs/ANTERIOR_VIEW_ROUTER_V1_BINARY_REVIEW.md`
