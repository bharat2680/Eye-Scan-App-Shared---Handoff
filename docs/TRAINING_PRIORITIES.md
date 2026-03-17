# Training Priorities

Last updated: 2026-03-17 08:58 Australia/Sydney

## Product truth

- the app already has an honest evaluation-only anterior screening pipeline
- the current live order is:
  1. `anterior_quality_gate_v1`
  2. `anterior_surface_binary_v2_simplecnn`
  3. `anterior_conjunctivitis_vs_normal_v1_simplecnn` only after
     `surface_abnormal`
  4. `anterior_cataract_vs_normal_v1_simplecnn` only after `normal_surface`
- the biggest remaining weakness is the still-broad fallback result:
  `Surface abnormality pattern detected`
- glaucoma can wait for now unless it is already mid-run

## Highest-priority next Dell work

Do next:

1. package and review `anterior_uveitis_vs_normal_v1_simplecnn`
2. package and review `anterior_pterygium_vs_normal_v1_simplecnn`
3. decide whether `anterior_eyelid_abnormality_vs_normal_v1_simplecnn`
   belongs in the same app branch or stays optional
4. gather cleaner external validation data for the new surface specialists

Why this order is best:

- `uveitis_vs_normal` has the strongest new local result after conjunctivitis
  while still having materially better support than `pterygium`
- `pterygium_vs_normal` looks excellent locally but has too little positive
  support to trust without caution
- `eyelid_abnormality_vs_normal` is usable, but it is not a clean replacement
  for the current surface-positive branch

## Fundus note from the latest Dell pass

- `fundus_router_v1_simplecnn` remains the strongest local fundus-side artifact
  with `test_accuracy=0.9819`
- simple reruns did not improve the disease specialists:
  - `fundus_glaucoma_vs_healthy_v2_balanced_simplecnn` rejected
  - `fundus_dr_vs_healthy_v2_balanced_simplecnn` rejected
  - `fundus_glaucoma_vs_healthy_v3_mobilenet` rejected
- the next useful fundus progress probably requires cleaner specialist data or a
  more substantial training recipe shift, not another minor SimpleCNN rerun

## Current local training status

- completed:
  - `anterior_conjunctivitis_vs_normal_v1_simplecnn`
  - `anterior_uveitis_vs_normal_v1_simplecnn`
  - `anterior_pterygium_vs_normal_v1_simplecnn`
  - `anterior_eyelid_abnormality_vs_normal_v1_simplecnn`
- all four remain `evaluation_only`
- packaged Mac-ready folders now exist under:
  `C:\Users\HP\OneDrive\Documents\Playground\handoff\macbook_next_specialist_packages`

## Exact rerun sequence

1. regenerate manifests:

```powershell
python scripts/prepare_manifests.py
```

2. rerun conjunctivitis specialist if needed:

```powershell
python training/anterior/train.py --config configs/anterior_conjunctivitis_vs_normal_v1_simplecnn.json
```

3. rerun uveitis specialist:

```powershell
python training/anterior/train.py --config configs/anterior_uveitis_vs_normal_v1_simplecnn.json
```

4. rerun pterygium specialist:

```powershell
python training/anterior/train.py --config configs/anterior_pterygium_vs_normal_v1_simplecnn.json
```

5. rerun eyelid specialist if still in scope:

```powershell
python training/anterior/train.py --config configs/anterior_eyelid_abnormality_vs_normal_v1_simplecnn.json
```

6. if any long run is interrupted, recover metrics from the saved checkpoint:

```powershell
python scripts/evaluate_checkpoint.py --config <config-path>
```

## Recommended app-side decision rule

- keep the current quality gate first
- keep the current `surface_abnormal` router first
- if `surface_abnormal`, keep `conjunctivitis` as the first narrower specialist
- review `uveitis` next, then `pterygium`
- only add `eyelid_abnormality` if the product explicitly wants eyelid findings
- only show a more specific evaluation-only label when the selected specialist
  threshold is met
- if no specific specialist clears threshold, keep the fallback wording:
  `Surface abnormality pattern detected`

## Required handoff for every specialist run

- exact dataset path
- exact manifest path
- exact config path
- exact artifact path
- label map
- preprocessing contract
- threshold strategy
- validation metrics
- test metrics
- deployment status
- intended use
- known failure modes

## Explicitly not recommended first

- another mixed all-anterior classifier
- exposing diagnosis language without routed gating
- glaucoma work ahead of the surface-specific anterior cleanup unless it is
  already mid-run
