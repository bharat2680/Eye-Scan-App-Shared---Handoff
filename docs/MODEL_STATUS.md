# Model Status

Last updated: 2026-03-16 22:55 Australia/Melbourne

## Current deployed anterior app pipeline

1. `anterior_quality_gate_v1`
2. `anterior_surface_binary_v2_simplecnn`
3. `anterior_cataract_vs_normal_v1_simplecnn`

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

## Main remaining weakness

`Surface abnormality pattern detected` is still broad because the surface model does not identify the exact condition.

## Recommended next model milestone

Add narrower anterior specialists after the current surface router:

1. conjunctivitis vs normal
2. pterygium vs normal
3. uveitis vs normal
4. eyelid abnormality vs normal

