# Codex Handoff

Last updated: 2026-03-17 00:07 Australia/Sydney

## Shared goal

Keep EyeScan honest while moving the vague surface-positive branch toward more
specific evaluation-only outputs.

## What the Mac side already has

- integrated:
  - `anterior_quality_gate_v1`
  - `anterior_surface_binary_v2_simplecnn`
  - `anterior_cataract_vs_normal_v1_simplecnn`
- live app can already show:
  - `Possible cataract pattern detected`
  - `Surface abnormality pattern detected`
  - `No screen-positive finding`
  - `Image quality needs recapture`

## What the Dell side has added since the last shared update

- exact manifests for:
  - `anterior_conjunctivitis_vs_normal_v1`
  - `anterior_uveitis_vs_normal_v1`
  - `anterior_pterygium_vs_normal_v1`
  - `anterior_eyelid_abnormality_vs_normal_v1`
- exact `SimpleCNN` configs for those four candidates
- one finished new specialist artifact:
  - `anterior_conjunctivitis_vs_normal_v1_simplecnn`

## Best current next specialist

### `anterior_conjunctivitis_vs_normal_v1_simplecnn`

- exact dataset path:
  `F:\datasets\Image Dataset on Eye Diseases Classification.zip`
- exact config path:
  `C:\Users\HP\OneDrive\Documents\Playground\configs\anterior_conjunctivitis_vs_normal_v1_simplecnn.json`
- exact artifact path:
  `C:\Users\HP\OneDrive\Documents\Playground\artifacts\anterior\anterior_conjunctivitis_vs_normal_v1_simplecnn`
- local package path on Dell:
  `C:\Users\HP\OneDrive\Documents\Playground\handoff\macbook_next_specialist_packages\anterior_conjunctivitis_vs_normal_v1_simplecnn_package`
- threshold:
  `0.15` on `p(conjunctivitis)`
- test summary:
  default `test_accuracy=0.9669`
  threshold-tuned `test_accuracy=0.9934`
  threshold-tuned confusion matrix `[[53, 1], [0, 97]]`
- deployment status:
  `evaluation_only`

## Recommended next Dell sequence

1. treat the conjunctivitis package as the first real follow-on candidate for
   the `surface_abnormal` branch
2. next train `anterior_uveitis_vs_normal_v1_simplecnn`
3. then train `anterior_pterygium_vs_normal_v1_simplecnn`
4. only then decide whether `anterior_eyelid_abnormality_vs_normal_v1_simplecnn`
   belongs in the same branch or should stay separate

## Important caution

- do not collapse back into a monolithic all-anterior classifier
- do not treat the current specialist outputs as medical diagnosis
- do not judge the latest PDF batch without separating:
  - `SCREENING_PIPELINE`
  - `TEST_MODE`
