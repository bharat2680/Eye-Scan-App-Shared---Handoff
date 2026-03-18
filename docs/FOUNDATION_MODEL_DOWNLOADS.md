# Foundation Model Downloads

Last updated: 2026-03-18 14:32 Australia/Sydney

## Why this exists

The current EyeScan workspace now has solid local baselines, but the next
meaningful accuracy lift is more likely to come from official pretrained
ophthalmic backbones than from another small rerun of the same local recipe.

This file defines the exact model downloads and target paths the Dell workspace
will expect next.

## Recommended download order

1. `VisionFM External Eye`
2. `VisionFM Slit Lamp`
3. `RETFound_dinov2_meh`
4. `VisionFM Fundus`

## Exact staging targets

### `VisionFM External Eye`

- exact staged weight path:
  `F:\datasets\FoundationModels\VisionFM\ExternalEye\visionfm_external_eye.pth`
- official source:
  `https://github.com/ABILab-CUHK/VisionFM`
- direct weight link from the official repo:
  `https://drive.google.com/file/d/16zGHTD4ZcGAYW382kKHBw3TU6D1OtvTD/view?usp=sharing`
- intended EyeScan use:
  first pretrained backbone candidate for the anterior quality gate and the
  surface-positive specialists
- why it is first:
  modality match is closest to EyeScan's smartphone-style anterior captures
- license note:
  VisionFM is released for research and educational use, not for unrestricted
  commercial deployment

### `VisionFM Slit Lamp`

- exact staged weight path:
  `F:\datasets\FoundationModels\VisionFM\SlitLamp\visionfm_slit_lamp.pth`
- official source:
  `https://github.com/ABILab-CUHK/VisionFM`
- direct weight link from the official repo:
  `https://drive.google.com/file/d/1kUZqj1ocviB8M8FnXXEmly6f7RrzVbJq/view?usp=drive_link`
- intended EyeScan use:
  comparison backbone for cataract and surface-specialist refinement
- caveat:
  still ophthalmic, but capture conditions are less similar to EyeScan phone
  images than the external-eye branch
- license note:
  research and educational use only

### `RETFound_dinov2_meh`

- exact staged weight path:
  `F:\datasets\FoundationModels\RETFound\Fundus\retfound_dinov2_meh.pth`
- official source:
  `https://github.com/rmaphoh/RETFound`
- official model hub:
  `https://huggingface.co/open-eye/RETFound`
- intended EyeScan use:
  primary official fundus pretrained backbone for the next DR and glaucoma
  experiments once curated external datasets are staged
- caveat:
  fundus only, so not for the anterior branch
- license note:
  the official RETFound release is non-commercial

### `VisionFM Fundus`

- exact staged weight path:
  `F:\datasets\FoundationModels\VisionFM\Fundus\visionfm_fundus.pth`
- official source:
  `https://github.com/ABILab-CUHK/VisionFM`
- direct weight link from the official repo:
  `https://drive.google.com/file/d/1H6I5UuROG5M3j8f-EE0rJHqVus-7LecV/view?usp=drive_link`
- intended EyeScan use:
  second official fundus backbone to compare against `RETFound`
- license note:
  research and educational use only

## Prepared validation helper

- `C:\Users\HP\OneDrive\Documents\Playground\scripts\check_foundation_model_staging.py`
- mirrored in the shared repo as:
  `scripts/check_foundation_model_staging.py`

Run after downloads are staged:

```powershell
python scripts/check_foundation_model_staging.py
```

## Latest staging verification

- checker run:
  `python scripts/check_foundation_model_staging.py`
- result:
  `0 / 4` present
- exact blocker:
  `F:\datasets\FoundationModels` does not exist yet
- interpretation:
  no VisionFM or RETFound transfer-learning run has started yet, and that is
  intentional because the required weights are still missing
- related note:
  newly inspected external fundus archives do not change this blocker because
  `Eye-Fundus.zip` is only a fallback dataset, `RFMiD2_0.zip` is missing
  labels, and the newer `1. Original Images.zip` is still image payload only

## Expected next Dell implementation step after download

1. verify staged files with the validation helper
2. add a PyTorch or `timm`-backed transfer-learning path beside the existing
   TensorFlow trainer
3. start with `VisionFM External Eye` on the anterior quality-gate and
   surface-positive branch
4. keep `RETFound` and `VisionFM Fundus` for the external fundus dataset wave

## Not recommended

- random third-party Kaggle checkpoints with unclear provenance
- another monolithic all-anterior model before the routed branch is improved
- promoting any foundation-model result without re-running the same honest
  evaluation-only packaging and threshold review used for the current models
