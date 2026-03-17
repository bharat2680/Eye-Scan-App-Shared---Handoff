# App Integration Status

Last updated: 2026-03-17 19:27 AEDT

## Current app-side behavior

The EyeScan iPhone build already uses an evaluation-only anterior screening
pipeline instead of the old quality-only stub.

Current backend sequence:

1. `anterior_quality_gate_v1`
2. `anterior_surface_binary_v2_simplecnn`
3. `anterior_conjunctivitis_vs_normal_v1_simplecnn` only when the surface
   model predicts `surface_abnormal`
4. `anterior_uveitis_vs_normal_v1_simplecnn` only when the surface model
   predicts `surface_abnormal` and conjunctivitis stays negative
5. `anterior_pterygium_vs_normal_v1_simplecnn` only when the surface model
   predicts `surface_abnormal` and both earlier surface specialists stay negative
6. `anterior_cataract_vs_normal_v1_simplecnn` only when the surface model
   predicts `normal_surface`

## Current backend result modes

- real backend result mode:
  `SCREENING_PIPELINE`
- simulated result mode:
  `TEST_MODE`

## App-side output now supported

- result screen shows screening summary plus quality score
- saved history stores screening metadata
- individual PDF export includes screening result when present
- multi-result PDF export includes screening result when present
- app/backend can now narrow some surface-positive cases to
  `Possible conjunctivitis pattern detected`
- app/backend can now narrow some surface-positive cases to
  `Possible uveitis pattern detected`
- app/backend can now narrow some surface-positive cases to
  `Possible pterygium pattern detected`

## Current local backend endpoints

- health:
  `http://<mac-lan-ip>:5050/health`
- legacy-compatible quality endpoint:
  `POST /inference/quality`
- routed evaluation endpoint:
  `POST /v1/predict`

## Current integrated surface-specific specialists

- `anterior_conjunctivitis_vs_normal_v1_simplecnn`
- `anterior_uveitis_vs_normal_v1_simplecnn`
- `anterior_pterygium_vs_normal_v1_simplecnn`
- status:
  all three remain `evaluation_only`
- current app role:
  they run only after `surface_abnormal` to narrow some broad surface-positive
  cases before the app falls back to `Surface abnormality pattern detected`

## Remaining optional Dell-side package not yet integrated

- `anterior_eyelid_abnormality_vs_normal_v1_simplecnn`
  package path on Dell:
  `C:\Users\HP\OneDrive\Documents\Playground\handoff\macbook_next_specialist_packages\anterior_eyelid_abnormality_vs_normal_v1_simplecnn_package`
- status:
  `evaluation_only`
- current recommendation:
  keep it optional unless eyelid findings are intentionally in product scope

## Recommended app-side follow-up

1. keep the current six-stage anterior pipeline stable for now
2. add a visible `TEST MODE` badge and prevent test-mode exports from being
   confused with real results
3. externally validate the integrated `uveitis` and `pterygium` heads before
   treating them as more than evaluation-only specialists
4. only pull `anterior_eyelid_abnormality_vs_normal_v1_simplecnn` into the app
   if eyelid findings are intentionally in scope
5. if no narrower specialist clears threshold, keep the fallback wording:
   `Surface abnormality pattern detected`
