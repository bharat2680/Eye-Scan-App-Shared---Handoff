# Eyelid View Routing Audit

Date: 2026-03-29

## Purpose

Document the current eyelid-related model state, the immediate live pipeline fix, and the recommended next-stage router design so clear eyelid-dominant photos do not get misrouted to conjunctivitis, uveitis, pterygium, or early recapture.

## Current State

- An existing eyelid specialist already exists:
  - `anterior_eyelid_abnormality_vs_normal_v1_simplecnn`
- It is suitable as an optional downstream eyelid abnormality specialist.
- It is **not** suitable as a view router.
- The missing component was a dedicated anterior view-routing decision between:
  - iris-visible images
  - eyelid-dominant images
  - unclear images

## Existing Eyelid Specialist Audit

### Dataset source

Desktop copy confirmed at:

`/Users/bharatsharma/Desktop/Image Dataset on Eye Diseases Classification (Uveitis, Conjunctivitis, Cataract, Eyelid) with Symptoms and SMOTE Validation`

Class folders present:

- `Cataract`
- `Conjunctivitis`
- `Eyelid`
- `Normal`
- `Pterygium`
- `Uveitis`

### Confirmed source counts

- Cataract: 544
- Conjunctivitis: 357
- Eyelid: 525
- Normal: 649
- Pterygium: 102
- Uveitis: 223

These counts exactly match the total sample counts implied by the packaged eyelid model split metrics:

- eyelid abnormality total: `367 + 79 + 79 = 525`
- normal total: `455 + 97 + 97 = 649`

This strongly confirms that the current eyelid specialist was trained from this dataset family.

### Synthetic / baked-in augmented files observed

The Desktop copy also contains many files with an `aug_` filename prefix:

- Cataract: 187
- Conjunctivitis: 39
- Eyelid: 84
- Normal: 0
- Pterygium: 0
- Uveitis: 30

Total detected `aug_` files: 340

Implication:

- this dataset can still help the router effort
- but it should **not** be reused blindly as a production routing dataset
- for Stage B, the router training set should prefer real captures first, with synthetic examples clearly controlled and tracked

### Current eyelid specialist labels

Packaged runtime label map:

- `eyelid_abnormality -> 0`
- `normal -> 1`

### Current eyelid specialist split counts

From packaged metrics:

- Train:
  - eyelid_abnormality: 367
  - normal: 455
- Validation:
  - eyelid_abnormality: 79
  - normal: 97
- Test:
  - eyelid_abnormality: 79
  - normal: 97

### Current eyelid specialist confusion

Default threshold:

- confusion matrix: `[[72, 7], [5, 92]]`

Threshold-tuned:

- confusion matrix: `[[74, 5], [8, 89]]`

Matrix order:

- `[eyelid_abnormality, normal]`

### Suitability verdict

#### 1. As an eyelid abnormality classifier

Yes, conditionally.

It is usable as:

- an optional evaluation-only specialist
- a downstream specialist after routing

It is not yet strong enough to be treated as a final clinic-grade answer by itself.

#### 2. As a view-type router

No.

Reasons:

- trained for `eyelid_abnormality` vs `normal`, not for `iris_visible` vs `eyelid_dominant` vs `unclear`
- no explicit `unclear` class
- no explicit objective to preserve eyelid-normal images as a valid non-iris route

## Stage A: Immediate Live Pipeline Improvement

### Exact insertion point

File:

`/Users/bharatsharma/FlutterProjects/eye_scan_app/backend/app.py`

Function:

`_run_prediction_pipeline_on_image(...)`

Insertion point:

After:

- quality gate result formatting
- eye/non-eye evidence normalization

Before:

- `surface_screen`
- conjunctivitis / uveitis / pterygium routing

### What Stage A does

1. Evaluate a lightweight heuristic anterior view type:
   - `iris_visible`
   - `eyelid_dominant`
   - `unclear`
2. If a photo is eyelid-dominant but was only failing for weak eye-presence / quality-model reasons:
   - apply a soft rescue
3. Once rescued as eyelid-dominant:
   - skip conjunctivitis
   - skip uveitis
   - skip pterygium
   - optionally run eyelid specialist only
4. If eyelid specialist is not strong enough:
   - return safe limited output instead of overcalling disease

### Stage A decision logic

```text
quality gate
  if hard failure unrelated to eye visibility:
    return recapture / unusable

eye / non-eye gate
  if non-eye:
    return no clear eye / recapture

view rescue check
  if eyelid-dominant evidence is strong enough:
    rescue borderline failures caused by weak eye-presence / quality-only rejection

if eyelid-dominant:
  run eyelid specialist only if available
  if eyelid specialist is strong:
    return possible eyelid abnormality
  else:
    return eyelid-limited result

if iris-visible:
  continue normal anterior routing:
    surface gate
    cataract or conjunctivitis / uveitis / pterygium / eyelid specialists

if unclear:
  return recapture guidance
```

### Stage A safe wording

Recommended limited output:

`Eyelid region detected — limited screening available. Capture the full eye including iris for broader screening.`

Recommended primary label:

`Eyelid region detected`

Recommended action:

- `retake_photo`

### Current live effect

The live backend now has:

- a soft eyelid rescue path
- a safe eyelid-limited output path
- explicit skipping of conjunctivitis / uveitis / pterygium for eyelid-dominant rescued images

## Stage B: New Lightweight Anterior View Router

### Goal

Build a dedicated production router that decides view type before specialist routing.

### Target labels

- `iris_visible`
- `eyelid_dominant`
- `unclear`

### Final desired production flow

```text
quality gate
-> eye / non-eye gate
-> anterior view router
-> specialist routing
```

Detailed:

```text
quality gate
  if unusable:
    return recapture

eye / non-eye gate
  if non-eye:
    return no clear eye

anterior view router
  if iris_visible:
    run surface + cataract / conjunctivitis / uveitis / pterygium / eyelid path
  if eyelid_dominant:
    run eyelid specialist only, or return eyelid-limited result
  if unclear:
    return recapture guidance
```

### Dataset requirements for new router

Target classes:

- `iris_visible`
- `eyelid_dominant`
- `unclear`

Recommended minimum pilot target:

- 1,000 images per class

Better production target:

- 1,500 to 2,000 images per class

Must include diversity across:

- skin tones
- age groups
- eye shapes
- device types
- lighting conditions
- partial eye views
- open / closed lids
- makeup / lashes / reflections

Important rule:

- `eyelid_dominant` must include both abnormal and normal eyelid-dominant images
- otherwise the router will learn `eyelid == disease`, which is not acceptable

### Augmentation rules

Allow:

- mild horizontal flip
- mild rotation
- mild zoom
- brightness / contrast jitter
- mild blur
- JPEG compression
- mild glare simulation

Avoid:

- aggressive crops that change the route label
- warps that fabricate iris visibility
- augmentations that convert valid iris-visible images into unclear examples

### Evaluation metrics

Primary:

- macro F1
- per-class precision / recall
- confusion matrix

Safety-critical targets:

- eyelid_dominant recall >= 0.95
- unclear recall >= 0.90
- eyelid_dominant misrouted to iris_visible < 2%

### Suggested deployment contract

```json
{
  "task": "anterior_view_router",
  "input": {
    "color_mode": "RGB",
    "image_size": [224, 224],
    "dtype": "float32",
    "resize": "direct_resize"
  },
  "output": {
    "predicted_label": "iris_visible | eyelid_dominant | unclear",
    "confidence": 0.0,
    "raw_scores": {
      "iris_visible": 0.0,
      "eyelid_dominant": 0.0,
      "unclear": 0.0
    },
    "decision_status": "route",
    "next_stage": "surface_specialists | eyelid_specialist | recapture"
  }
}
```

## UI / Labels / PDFs

### Current Details screen

Yes, the Details screen should use user-friendly mode labels instead of raw backend labels.

Preferred user-facing labels:

- `Anterior screening`
- `Fundus screening`
- `Saved result`
- `Limited eyelid screening`

Avoid showing raw backend labels like:

- `SCREENING_PIPELINE`
- `FUNDUS_MULTI_SPECIALIST_SCREENING`

### PDF changes

No mandatory PDF contract change is required for Stage A.

However, if the eyelid-limited output is shown in exports, preferred wording is:

- Result:
  - `Eyelid region detected — limited screening available`
- What this means:
  - `The image appears eyelid-dominant, so broader iris-dependent screening was not applied. Capture the full eye including iris for broader screening.`
- Recommended next step:
  - `Retake the photo with the full eye including iris`

## Recommended Next Steps

1. Keep the current eyelid abnormality model as downstream specialist only.
2. Keep the new live rescue path active.
3. Do not retrain the current eyelid abnormality model immediately.
4. Build a separate lightweight anterior view router.
5. Once router metrics are strong enough:
   - replace heuristic view rescue with learned routing
   - keep the eyelid specialist downstream
