# App Integration Status

Last updated: 2026-03-23 21:36 AEDT

## Current app-side behavior

The EyeScan iPhone build already uses an evaluation-only anterior screening
pipeline instead of the old quality-only stub.

Current backend sequence:

1. `eye_vs_non_eye_gate_v1_simplecnn`
2. `anterior_quality_gate_v1`
3. `anterior_surface_binary_v2_simplecnn`
4. `anterior_conjunctivitis_vs_normal_v1_simplecnn` only when the surface
   model predicts `surface_abnormal`
5. `anterior_uveitis_vs_normal_v1_simplecnn` only when the surface model
   predicts `surface_abnormal` and conjunctivitis stays negative
6. `anterior_pterygium_vs_normal_v1_simplecnn` only when the surface model
   predicts `surface_abnormal` and both earlier surface specialists stay negative
7. `anterior_cataract_vs_normal_v1_simplecnn` only when the surface model
   predicts `normal_surface`

Live backend version:

- `anterior_screening_eval_v7`

## Current backend result modes

- real backend result mode:
  `SCREENING_PIPELINE`
- simulated result mode:
  `TEST_MODE`

Recent app-side hardening:

- a dedicated eye-vs-non-eye blocker now runs before the quality gate so
  obvious laptop, family-photo, and other non-eye captures can be stopped
  before they reach the anterior routing stack
- the old heuristic eye detector is still kept as a secondary signal, but the
  new blocker can now rescue some real-eye captures that the heuristic would
  have rejected
- backend now blocks specialist screening if no clear eye is detected, even if
  the learned quality probability is high
- the eye-feature gate was relaxed enough to keep some angled real-eye photos
  while still rejecting clearly non-eye images more aggressively
- backend now also applies a dark-band rejection check to better stop laptop
  and screen captures from leaking into the surface-specialist branch
- simulated outputs are now labeled as `Simulated demo result` in the app,
  saved results, and exported PDFs
- the yellow in-app demo banner now uses dark text for readability on the dark
  theme

## App-side output now supported

- result screen shows screening summary plus quality score
- saved history stores screening metadata
- individual PDF export includes screening result when present
- multi-result PDF export includes screening result when present
- single-result and multi-result PDFs now include:
  - a centered `EyeScan / EYE HEALTH AI` text watermark
  - symbol-logo marks on both sides of the image row near the top
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

## Current monetization scaffold

- Android Play Billing support is now integrated using Flutter
  `in_app_purchase`
- the app now exposes a clinic access screen from settings and the about screen
- default Play product IDs currently compiled into the app are:
  - subscription: `eyescan_plus`
- PDF export and multi-result PDF export can be access-gated, but gating is
  currently disabled by default through:
  `EYESCAN_PREMIUM_GATING_ENABLED=false`
- trial defaults currently compiled into the app are:
  - `14` days
  - `100` scans
  - `2` authorised users
- latest billing-enabled Android bundle built locally:
  `1.1.6+15`
- current limitation:
  entitlement handling is still local-device based for first release/testing
  and does not yet include backend clinic-trial enforcement or server-side
  receipt validation

## Current branding state

- app icon asset is now the symbol-only EyeScan digital mark
- white launch screen asset is now the full `EyeScan / Eye Health AI` artwork
- launcher icons and native splash assets were regenerated on the Mac from
  those updated source files

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
2. keep the new explicit `TEST MODE` labeling and demo-only export wording so
   simulated runs are not confused with live backend results
3. externally validate the integrated `uveitis` and `pterygium` heads before
   treating them as more than evaluation-only specialists
4. only pull `anterior_eyelid_abnormality_vs_normal_v1_simplecnn` into the app
   if eyelid findings are intentionally in scope
5. if no narrower specialist clears threshold, keep the fallback wording:
   `Surface abnormality pattern detected`
6. rerun the current non-eye regression check on-device against the `eval_v6`
   backend before making more model changes
7. ask the Dell training lane for a dedicated `anterior_eye_presence_gate_v1`
   so obvious non-eye captures are rejected before the quality gate instead of
   relying only on heuristic hardening
8. keep the new eye-vs-non-eye blocker in `evaluation_only` status until it
   has been exercised on more real tester photos and public-backend beta runs
