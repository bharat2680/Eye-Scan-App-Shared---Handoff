# Model Status

Last updated: 2026-03-17 00:07 Australia/Sydney

## Current integrated anterior app pipeline

1. `anterior_quality_gate_v1`
2. `anterior_surface_binary_v2_simplecnn`
3. `anterior_cataract_vs_normal_v1_simplecnn` only after `normal_surface`

## Integrated model roles

### `anterior_quality_gate_v1`

- role:
  quality pass/fail only
- deployment status:
  integrated

### `anterior_surface_binary_v2_simplecnn`

- output labels:
  `normal_surface`, `surface_abnormal`
- decision rule:
  plain `argmax`
- validation metrics:
  `val_accuracy=0.9849`, `val_loss=0.0611`
- test metrics:
  `test_accuracy=0.9950`
  confusion matrix `[[96, 1], [0, 102]]`
- deployment status:
  integrated as `evaluation_only`

### `anterior_cataract_vs_normal_v1_simplecnn`

- output labels:
  `cataract`, `normal`
- decision rule:
  positive label `cataract`
  threshold `0.15` on `p(cataract)`
- validation metrics:
  `val_accuracy=0.8958`, `val_loss=0.2602`
  threshold-tuned `balanced_accuracy=0.9273`
- test metrics:
  default `test_accuracy=0.9553`
  threshold-tuned `test_accuracy=0.9609`
  threshold-tuned confusion matrix `[[80, 2], [5, 92]]`
- deployment status:
  integrated as `evaluation_only`

## New Dell-side candidate artifact

### `anterior_conjunctivitis_vs_normal_v1_simplecnn`

- exact dataset path:
  `F:\datasets\Image Dataset on Eye Diseases Classification.zip`
- exact manifest path:
  `C:\Users\HP\OneDrive\Documents\Playground\datasets\manifests\anterior_conjunctivitis_vs_normal_v1.jsonl`
- exact config path:
  `C:\Users\HP\OneDrive\Documents\Playground\configs\anterior_conjunctivitis_vs_normal_v1_simplecnn.json`
- exact artifact path:
  `C:\Users\HP\OneDrive\Documents\Playground\artifacts\anterior\anterior_conjunctivitis_vs_normal_v1_simplecnn`
- label map:
  `conjunctivitis -> 0`, `normal -> 1`
- preprocessing:
  RGB, `224 x 224`, direct resize, `float32`, internal `Rescaling(1.0 / 255.0)`
- decision rule:
  positive label `conjunctivitis`
  threshold `0.15` on `p(conjunctivitis)`
- validation metrics:
  `val_accuracy=0.9875`, `val_loss=0.0920`
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
  surface-positive results to
  `Possible conjunctivitis pattern detected`
- known failure modes:
  single-source bootstrap training only and likely overlap with other red-eye
  causes not labeled separately here

## Main remaining weakness

`Surface abnormality pattern detected` is still broad whenever no narrower
surface specialist is available or confident enough.

## Exact next specialist queue

### `anterior_uveitis_vs_normal_v1_simplecnn`

- dataset path:
  `F:\datasets\Image Dataset on Eye Diseases Classification.zip`
- config path:
  `C:\Users\HP\OneDrive\Documents\Playground\configs\anterior_uveitis_vs_normal_v1_simplecnn.json`
- artifact path:
  `C:\Users\HP\OneDrive\Documents\Playground\artifacts\anterior\anterior_uveitis_vs_normal_v1_simplecnn`
- deployment status:
  `not_run_yet`

### `anterior_pterygium_vs_normal_v1_simplecnn`

- dataset path:
  `F:\datasets\Image Dataset on Eye Diseases Classification.zip`
- config path:
  `C:\Users\HP\OneDrive\Documents\Playground\configs\anterior_pterygium_vs_normal_v1_simplecnn.json`
- artifact path:
  `C:\Users\HP\OneDrive\Documents\Playground\artifacts\anterior\anterior_pterygium_vs_normal_v1_simplecnn`
- deployment status:
  `not_run_yet`

### `anterior_eyelid_abnormality_vs_normal_v1_simplecnn`

- dataset path:
  `F:\datasets\Image Dataset on Eye Diseases Classification.zip`
- config path:
  `C:\Users\HP\OneDrive\Documents\Playground\configs\anterior_eyelid_abnormality_vs_normal_v1_simplecnn.json`
- artifact path:
  `C:\Users\HP\OneDrive\Documents\Playground\artifacts\anterior\anterior_eyelid_abnormality_vs_normal_v1_simplecnn`
- deployment status:
  `not_run_yet`
