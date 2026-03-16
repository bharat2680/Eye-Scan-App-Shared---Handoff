# App Integration Status

Last updated: 2026-03-16 22:55 Australia/Melbourne

## Current app-side behavior

The EyeScan iPhone build now uses an app-local anterior screening pipeline instead of the old quality-only stub.

Current backend sequence:

1. anterior quality gate
2. anterior surface routing model
3. cataract-vs-normal model only when the surface model predicts `normal_surface`

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

## Current local backend endpoints

- health:
  `http://<mac-lan-ip>:5050/health`
- legacy-compatible quality endpoint:
  `POST /inference/quality`
- routed evaluation endpoint:
  `POST /v1/predict`

## Validation completed on the Mac

- `python3 -m unittest backend.test_app` passed
- `flutter test` passed
- `flutter analyze` passed
- live backend health check confirmed all three integrated components are available

## Recommended app-side follow-up

1. Add a visible `TEST MODE` badge and prevent test-mode exports from being confused with real results.
2. Separate or clear saved history before formal export evidence runs.
3. Add narrower anterior specialists after the surface router so surface-positive results become less vague.

