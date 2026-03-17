# Model Status

Last updated: 2026-03-17 15:13 Australia/Sydney

## Current integrated anterior app pipeline

1. `anterior_quality_gate_v1`
2. `anterior_surface_binary_v2_simplecnn`
3. `anterior_conjunctivitis_vs_normal_v1_simplecnn` only after `surface_abnormal`
4. `anterior_cataract_vs_normal_v1_simplecnn` only after `normal_surface`

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

## New Dell-side specialist artifacts ready for Mac review

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
- intended use:
  optional separate specialist only if eyelid findings remain in product scope
- known failure modes:
  not a clean surface-only head, depends on eyelid visibility in framing, and
  the selected validation threshold generalized slightly worse than plain
  `argmax` on the held-out local test split

## Best next Mac review order

1. keep the current integrated four-stage anterior pipeline stable
2. review `anterior_uveitis_vs_normal_v1_simplecnn` as the next surface-positive
   candidate after conjunctivitis
3. review `anterior_pterygium_vs_normal_v1_simplecnn` next, but keep it
   explicitly cautious because of tiny local support
4. only pull `anterior_eyelid_abnormality_vs_normal_v1_simplecnn` into the app
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
