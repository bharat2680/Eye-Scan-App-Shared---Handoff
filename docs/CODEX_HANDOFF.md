# EyeScan Codex Handoff

Last updated: 2026-03-17 22:52 Australia/Sydney

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
  `anterior_screening_eval_v4`

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
4. only add `anterior_eyelid_abnormality_vs_normal_v1_simplecnn` if eyelid
   findings remain intentionally in scope
5. if no narrower specialist clears threshold, keep the fallback wording:
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

Current blocker:

- those official weight files are not on `F:\datasets` yet
- the local trainer is still TensorFlow-only, so Dell-side implementation will
  add a PyTorch or `timm`-based transfer-learning path once the files arrive

Latest staging verification:

- ran:
  `python scripts/check_foundation_model_staging.py`
- result:
  `0 / 4` present
- exact blocker:
  `F:\datasets\FoundationModels` does not exist yet
- status:
  no transfer-learning artifact has been started from this lane because the
  weights are still missing

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
