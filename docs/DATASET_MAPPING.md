# Dataset Mapping

Last updated: 2026-03-17 16:08 Australia/Sydney

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
- deployment status:
  `pending_dataset`

### `fundus_glaucoma_papila_v1`

- exact dataset path:
  `F:\datasets\External Fundus\PAPILA_Glaucoma_vs_Healthy`
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
- deployment status:
  `pending_dataset`
