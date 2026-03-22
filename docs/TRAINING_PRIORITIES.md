# Training Priorities

Last updated: 2026-03-22 22:39 AEDT

## Product truth

- the app already has an honest evaluation-only anterior screening pipeline
- the current live order is:
  1. `anterior_quality_gate_v1`
  2. `anterior_surface_binary_v2_simplecnn`
  3. `anterior_conjunctivitis_vs_normal_v1_simplecnn` only after
     `surface_abnormal`
  4. `anterior_uveitis_vs_normal_v1_simplecnn` only after `surface_abnormal`
     and only when conjunctivitis stays negative
  5. `anterior_pterygium_vs_normal_v1_simplecnn` only after
     `surface_abnormal` and only when the earlier surface specialists stay
     negative
  6. `anterior_cataract_vs_normal_v1_simplecnn` only after `normal_surface`
- the biggest remaining weakness is the still-broad fallback result:
  `Surface abnormality pattern detected`
- glaucoma can wait for now unless it is already mid-run

## Highest-priority next Dell work

Do next:

1. keep app release and version-code work untouched from this Dell lane
2. train a dedicated `anterior_eye_presence_gate_v1` so obvious non-eye
   captures are rejected before the quality gate and specialist routing
3. compare the new VisionFM external-eye quality-gate candidate against
   `anterior_quality_gate_v1` and `anterior_quality_gate_v2_teyeds_simplecnn`
   on real EyeScan captures
4. keep the Colab notebook and Dell-side training lane aligned now that the
   first VisionFM transfer-learning run has succeeded
5. gather broader validation data for the already-integrated
   `anterior_uveitis_vs_normal_v1_simplecnn`
6. gather broader validation data for the already-integrated
   `anterior_pterygium_vs_normal_v1_simplecnn` with explicit caution on low
   support
7. decide whether `anterior_eyelid_abnormality_vs_normal_v1_simplecnn`
   belongs in the same app branch or stays optional
8. gather cleaner external validation data for the new surface specialists
9. start the better fundus-data wave using the prepared external staging paths
   and configs below
10. review the new TEyeDS-backed quality-gate candidate before changing the live
   front gate
11. keep the older VisionFM refined-classifier pilot separate from the new
    single-task quality-gate linear-probe candidate

Why this order is best:

- the app still sees occasional non-eye or weak-eye edge cases, so a dedicated
  eye-presence gate is a cleaner next fix than forcing the quality gate to
  absorb every possible hard negative
- `uveitis_vs_normal` has the strongest new local result after conjunctivitis
  while still having materially better support than `pterygium`
- `pterygium_vs_normal` looks excellent locally but has too little positive
  support to trust without caution
- `eyelid_abnormality_vs_normal` is usable, but it is not a clean replacement
  for the current surface-positive branch
- the new VisionFM external-eye run is now a real packaged evaluation
  candidate, but it still needs app-side comparison on real captures
- the older VisionFM refined pilot remains useful as a research direction, but
  it is still a Colab/Drive-side artifact rather than a backend-ready package

## Requested dedicated eye-presence gate

- requested artifact name:
  `anterior_eye_presence_gate_v1`
- purpose:
  hard-reject obvious non-eye captures before the quality gate
- preferred labels:
  - `eye_present`
  - `non_eye`
- preferred negative examples:
  laptops, monitors, keyboards, phones, tablets, circular toys, balls,
  planets, stars, moon-like imagery, water reflections, glossy household
  objects, printed eyes, and on-screen eye photos
- practical Mac-side reason:
  the current heuristic hardening improved things, but it is still a rules
  patch; a dedicated learned rejector is the cleaner long-term fix
- deployment target:
  package it for Mac review first and keep it `evaluation_only`

## Fundus note from the latest Dell pass

- `fundus_router_v1_simplecnn` remains the strongest local fundus-side artifact
  with `test_accuracy=0.9819`
- local disease-specialist reruns still did not improve enough to promote:
  - `fundus_glaucoma_vs_healthy_v2_balanced_simplecnn` rejected
  - `fundus_dr_vs_healthy_v2_balanced_simplecnn` rejected
  - `fundus_glaucoma_vs_healthy_v3_mobilenet` rejected
  - `fundus_glaucoma_vs_healthy_v4_mobilenet_headonly` rejected
  - `fundus_dr_vs_healthy_v3_mobilenet_headonly` rejected
- the two head-only MobileNet transfer-learning runs also collapsed to the
  disease class, so the next useful fundus progress probably requires cleaner
  specialist data or a larger recipe change, not another local baseline rerun

## External fundus inspection note from this pass

- `Eye-Fundus.zip` is usable as a fallback local fundus source while the
  official foundation-model lane is still blocked
- best immediate future derivations from that archive are
  `diabetic_retinopathy_vs_healthy` and `glaucoma_vs_healthy`
- caveat:
  it is a rehosted single-label archive with pre-resized `224 x 224` images
  and some trailing spaces in internal label-folder names
- `RFMiD2_0.zip` is not trainable yet from the current download because the
  archive contains split image zips but no label CSV or annotation file
- `1. Original Images.zip` is now confirmed as a complete RFMiD image payload
  once paired with the downloaded train, validation, and testing label CSVs
- inspected shape:
  `3,200` PNG images with train `1,920`, val `640`, and test `640`
- label shape:
  `47` columns total with `45` disease label columns plus `Disease_Risk`
- practical use:
  this now gives the Dell side a real trainable RFMiD package for later fundus
  experiments once the recipe is selected
- `archive (1).zip` is a separate ARMD-only image archive, not the missing
  RFMiD annotations
- this means the fundus side now has one usable fallback archive and one still
  incomplete archive, plus one now-complete RFMiD package, but fundus still is
  not the immediate priority while the new VisionFM anterior gate is under
  review

## Prepared external fundus path

Staging roots expected on the dataset drive:

- `F:\datasets\External Fundus\IDRiD_DR_vs_Healthy`
- `F:\datasets\External Fundus\REFUGE_Glaucoma_vs_Healthy`
- `F:\datasets\External Fundus\PAPILA_Glaucoma_vs_Healthy`

Prepared manifest tooling:

- `C:\Users\HP\OneDrive\Documents\Playground\scripts\build_directory_manifest.py`
- `C:\Users\HP\OneDrive\Documents\Playground\scripts\prepare_external_manifests.py`

Prepared configs:

- `C:\Users\HP\OneDrive\Documents\Playground\configs\fundus_dr_idrid_v1_simplecnn.json`
- `C:\Users\HP\OneDrive\Documents\Playground\configs\fundus_glaucoma_refuge_v1_simplecnn.json`
- `C:\Users\HP\OneDrive\Documents\Playground\configs\fundus_glaucoma_papila_v1_simplecnn.json`

Exact next sequence once those staged folders exist:

1. build manifests:

```powershell
python scripts/prepare_external_manifests.py
```

2. train DR on IDRiD:

```powershell
python training/fundus/train.py --config configs/fundus_dr_idrid_v1_simplecnn.json
```

3. train glaucoma on REFUGE:

```powershell
python training/fundus/train.py --config configs/fundus_glaucoma_refuge_v1_simplecnn.json
```

4. train glaucoma on PAPILA as a second specialist check:

```powershell
python training/fundus/train.py --config configs/fundus_glaucoma_papila_v1_simplecnn.json
```

Current status of this path:

- manifests are scaffolded but not built yet because the staged dataset
  folders do not exist on `F:\datasets`
- deployment status for these external runs is `pending_dataset`

## Current local training status

- completed:
  - `anterior_quality_gate_v2_teyeds_simplecnn`
  - `anterior_conjunctivitis_vs_normal_v1_simplecnn`
  - `anterior_uveitis_vs_normal_v1_simplecnn`
  - `anterior_pterygium_vs_normal_v1_simplecnn`
  - `anterior_eyelid_abnormality_vs_normal_v1_simplecnn`
- all five remain `evaluation_only`
- packaged Mac-ready folders now exist under:
  `C:\Users\HP\OneDrive\Documents\Playground\handoff\macbook_next_specialist_packages`

## Quality-gate note from the latest Dell pass

- `anterior_quality_gate_v2_teyeds_simplecnn` is now the best new gate
  candidate produced in this pass
- dataset root:
  `C:\Users\HP\OneDrive\Documents\Playground\datasets\teyeds_quality_gate_v1`
- manifest path:
  `C:\Users\HP\OneDrive\Documents\Playground\datasets\manifests\anterior_quality_gate_v2_teyeds.jsonl`
- config path:
  `C:\Users\HP\OneDrive\Documents\Playground\configs\anterior_quality_gate_v2_teyeds_simplecnn.json`
- artifact path:
  `C:\Users\HP\OneDrive\Documents\Playground\artifacts\anterior\anterior_quality_gate_v2_teyeds_simplecnn`
- package path:
  `C:\Users\HP\OneDrive\Documents\Playground\handoff\macbook_quality_gate_packages\anterior_quality_gate_v2_teyeds_simplecnn_package`
- default test accuracy:
  `0.8256`
- threshold-tuned test balanced accuracy:
  `0.7984`
- threshold-tuned `needs_recapture` recall:
  `0.7467`
- recommendation:
  review against real EyeScan captures before replacing `anterior_quality_gate_v1`

## VisionFM quality-gate pilot note

- a new VisionFM-based pilot quality gate now exists as a two-stage artifact:
  1. VisionFM backbone checkpoint
  2. refined sklearn LogisticRegression classifier
- reproducible notebook path on the Mac:
  `/Users/bharatsharma/Desktop/Google Console/Vision FM Files/VisionFM_Pilot.ipynb`
- provided handoff paths:
  - `/content/drive/MyDrive/Datasets/VFM Datasets/VFM_External_weights.pth`
  - `/content/drive/MyDrive/EyeScan_Models/visionfm_quality_classifier_refined.pkl`
  - `/content/drive/MyDrive/EyeScan_Models/visionfm_quality_label_map_refined.json`
  - `/content/drive/MyDrive/EyeScan_Models/visionfm_quality_metadata_labeled.csv`
  - `/content/drive/MyDrive/EyeScan_Models/visionfm_quality_handoff_summary.json`
- refined classes:
  - `bad`
  - `glare_lighting`
  - `good_centered`
  - `off_angle`
- purpose:
  pilot quality gate built on VisionFM embeddings plus LogisticRegression from
  TEyeD extracted images
- strict instruction:
  do not integrate into `erica_server.py` or the live backend yet unless
  explicitly approved later
- practical next step:
  first reconcile the base `.pth` checkpoint with the shared
  `FoundationModels/VisionFM/ExternalEye` staging lane, then repackage this as
  a reproducible evaluation candidate before considering backend integration
- notebook-confirmed structure:
  the notebook both extracts embeddings and trains the refined classifier, so
  future reruns should prefer the notebook as the canonical recipe instead of
  reconstructing the steps from chat

## VisionFM external-eye quality-gate candidate

- a first Colab-based VisionFM external-eye linear-probe run is now complete
- exact notebook path:
  `Google Colab/Quality Gate/anterior_quality_gate_v3_visionfm_external_linearprobe.ipynb`
- exact Drive output folder:
  `/content/drive/MyDrive/EyeScan_Models/VisionFM_Quality_Gate_V3`
- exact backbone path:
  `/content/drive/MyDrive/Datasets/VFM Datasets/VFM_External_weights.pth`
- preferred Mac handoff package:
  `F:\EyeScan App\Datasets\VisionFM_Quality_Gate_V3_mac_handoff.zip`
- full package for deeper inspection:
  `F:\EyeScan App\Datasets\VisionFM_Quality_Gate_V3_package.zip`
- default test accuracy:
  `0.9133`
- threshold-tuned test accuracy:
  `0.9337`
- selected threshold:
  `0.25` on `p(needs_recapture)`
- threshold-tuned `needs_recapture` recall:
  `1.0000`
- recommendation:
  keep it `evaluation_only` and compare against real EyeScan captures before
  any app-side gate replacement decision

## Official foundation-model downloads to stage next

These are the best next internet-sourced model weights to stage on the dataset
drive before the next recipe change:

1. `VisionFM External Eye`
2. `VisionFM Slit Lamp`
3. `RETFound_dinov2_meh`
4. `VisionFM Fundus`

Why this order is best:

- `VisionFM External Eye` is the closest modality match to EyeScan's
  smartphone-style anterior captures, so it is the best first bet for the
  quality gate and the surface-abnormal specialists
- `VisionFM Slit Lamp` is still relevant for anterior pathology, but it has
  more capture mismatch than the external-eye branch
- `RETFound_dinov2_meh` and `VisionFM Fundus` are better saved for the staged
  external fundus wave once those curated folder datasets exist

Exact staging targets:

- `F:\datasets\FoundationModels\VisionFM\ExternalEye\visionfm_external_eye.pth`
- `F:\datasets\FoundationModels\VisionFM\SlitLamp\visionfm_slit_lamp.pth`
- `F:\datasets\FoundationModels\RETFound\Fundus\retfound_dinov2_meh.pth`
- `F:\datasets\FoundationModels\VisionFM\Fundus\visionfm_fundus.pth`

Prepared validation helper:

- `C:\Users\HP\OneDrive\Documents\Playground\scripts\check_foundation_model_staging.py`
- mirrored in the shared repo as:
  `scripts/check_foundation_model_staging.py`

Current status on this path:

- the canonical `F:\datasets\FoundationModels` root is still absent
- but the updated Dell-side checker now resolves all four official weights in
  the alternate EyeScan dataset location
- latest verifier result:
  `4 / 4` present
- current practical state:
  the VisionFM transfer-learning lane is no longer blocked on missing weights
  and already has its first real anterior quality-gate candidate

Latest verifier result:

- ran:
  `python scripts/check_foundation_model_staging.py`
- result:
  `4 / 4` present
- resolved alternate paths:
  - `F:\Datasets\External Fundus\VFM Datasets\VFM_External_weights.pth`
  - `F:\Datasets\External Fundus\VFM Datasets\VFM_SiltLamp_weights.pth`
  - `F:\Datasets\External Fundus\VFM Datasets\RET Found Dino V2\RETFound_dinov2_meh.pth`
  - `F:\Datasets\External Fundus\VFM Datasets\VFM_Fundus_weights.pth`

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
- keep `uveitis` next, then `pterygium`
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
