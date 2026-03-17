# EyeScan Codex Handoff

Last updated: 2026-03-17 19:27 AEDT

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

- glaucoma work unless it is already mid-run
- fundus cleanup ahead of the anterior surface-specificity gap

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
