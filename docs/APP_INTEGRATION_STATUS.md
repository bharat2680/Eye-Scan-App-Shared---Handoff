# App Integration Status

Last updated: 2026-03-17 08:58 Australia/Sydney

## Current app-side behavior

The EyeScan iPhone build already uses an evaluation-only anterior screening
pipeline instead of the old quality-only stub.

Current backend sequence:

1. `anterior_quality_gate_v1`
2. `anterior_surface_binary_v2_simplecnn`
3. `anterior_conjunctivitis_vs_normal_v1_simplecnn` only when the surface
   model predicts `surface_abnormal`
4. `anterior_cataract_vs_normal_v1_simplecnn` only when the surface model
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

## Current local backend endpoints

- health:
  `http://<mac-lan-ip>:5050/health`
- legacy-compatible quality endpoint:
  `POST /inference/quality`
- routed evaluation endpoint:
  `POST /v1/predict`

## Current integrated surface-specific specialist

- `anterior_conjunctivitis_vs_normal_v1_simplecnn`
- status:
  `evaluation_only`
- current app role:
  runs only after `surface_abnormal` to narrow some broad surface-positive
  cases into `Possible conjunctivitis pattern detected`

## New Dell-side packages now ready for Mac review

- `anterior_uveitis_vs_normal_v1_simplecnn`
  package path on Dell:
  `C:\Users\HP\OneDrive\Documents\Playground\handoff\macbook_next_specialist_packages\anterior_uveitis_vs_normal_v1_simplecnn_package`
- `anterior_pterygium_vs_normal_v1_simplecnn`
  package path on Dell:
  `C:\Users\HP\OneDrive\Documents\Playground\handoff\macbook_next_specialist_packages\anterior_pterygium_vs_normal_v1_simplecnn_package`
- `anterior_eyelid_abnormality_vs_normal_v1_simplecnn`
  package path on Dell:
  `C:\Users\HP\OneDrive\Documents\Playground\handoff\macbook_next_specialist_packages\anterior_eyelid_abnormality_vs_normal_v1_simplecnn_package`

These are all still `evaluation_only`. The best next app candidate after the
already-integrated conjunctivitis head is `anterior_uveitis_vs_normal_v1_simplecnn`.

## Recommended app-side follow-up

1. keep the current four-stage anterior pipeline stable for now
2. add a visible `TEST MODE` badge and prevent test-mode exports from being
   confused with real results
3. review `anterior_uveitis_vs_normal_v1_simplecnn` next for the
   `surface_abnormal` branch
4. review `anterior_pterygium_vs_normal_v1_simplecnn` after that, with
   explicit caution on low sample support
5. only pull `anterior_eyelid_abnormality_vs_normal_v1_simplecnn` into the app
   if eyelid findings are intentionally in scope
6. if no narrower specialist clears threshold, keep the fallback wording:
   `Surface abnormality pattern detected`
