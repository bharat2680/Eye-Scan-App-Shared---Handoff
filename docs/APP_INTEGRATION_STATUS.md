# App Integration Status

Last updated: 2026-04-03 23:34 AEDT

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
7. `anterior_eyelid_abnormality_vs_normal_v1_simplecnn` only when the surface
   model predicts `surface_abnormal` and all earlier surface specialists stay negative
8. `anterior_cataract_vs_normal_v1_simplecnn` only when the surface model
   predicts `normal_surface`

Live backend version:

- `anterior_screening_eval_v9`
- separate multi-specialist fundus route now available when
  `requested_modality=fundus` is sent to `POST /v1/predict`
- current fundus DR specialist:
  `fundus_dr_idrid_v3_efficientnetb2_balanced_colab`
- current fundus glaucoma fallback model:
  `fundus_glaucoma_eyefundus_v3_efficientnetb0_colab`
- current fundus DR package path:
  `/Users/bharatsharma/FlutterProjects/eye_scan_app/backend/model_packages/fundus_dr_idrid_v3_efficientnetb2_balanced_colab_package`
- current fundus glaucoma package path:
  `/Users/bharatsharma/FlutterProjects/eye_scan_app/backend/model_packages/fundus_glaucoma_eyefundus_v3_efficientnetb0_colab_package`

## Current backend result modes

- real backend result mode:
  `SCREENING_PIPELINE`
- simulated result mode:
  `TEST_MODE`
- additional fundus legacy mode:
  `FUNDUS_MULTI_SPECIALIST_SCREENING`

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
- backend now supports an evaluation-only multi-specialist fundus branch behind
  `requested_modality=fundus`, and that branch currently runs both the
  `IDRiD` diabetic-retinopathy specialist and the fallback glaucoma specialist
- when both fundus specialists fire on the same image, the backend now keeps
  diabetic retinopathy as the primary summary and leaves the fallback glaucoma
  hit visible as secondary evidence in metadata instead of over-promoting a
  combined diagnosis
- public fundus arbitration is now stricter:
  strong healthy confidence can override weaker glaucoma-only spikes, and
  glaucoma positives now require both higher confidence and a healthier margin
  over the healthy signal before they are exported as positive
- the current mobile capture flow still defaults to anterior screening unless
  the caller explicitly requests fundus

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
- fundus fallback trigger:
  send `requested_modality=fundus` to `POST /v1/predict`
- optional fundus subtype hints:
  `requested_modality=fundus_dr` or `requested_modality=fundus_glaucoma`

## Current public beta backend

- Cloud Run service:
  `eyescan-backend-beta`
- public backend URL:
  `https://eyescan-backend-beta-66791987039.australia-southeast2.run.app`
- public health endpoint:
  `https://eyescan-backend-beta-66791987039.australia-southeast2.run.app/health`
- current beta deployment role:
  public tester screening outside the local Wi-Fi network
- latest backend refresh:
  public Cloud Run backend was redeployed on `2026-04-03` with the newer
  strict staged routing flow plus stricter fundus false-positive control
- current public revision:
  `eyescan-backend-beta-00006-pf6`

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
  `1.1.7+17`
- current Android release state:
  production release `17 (1.1.7)` has been uploaded in Google Play Console and
  sent for review
- current public-backend fix:
  release-hardened builds now fall back to the public Cloud Run backend URL
  so Android testers without a manually entered LAN backend should reach real
  screening instead of saving fake `0%` placeholder results
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
6. wait for Google Play review on Android production build `17 (1.1.7)` to
   complete, then confirm the live store artifact shows newest-first recent
   scans ordering on device
7. do one more healthy-fundus phone-capture spot check against the updated
   public backend to confirm the stricter glaucoma margin behaves well on
   obviously normal retina images
8. rerun the current non-eye regression check on-device against the updated
   public backend before making more model changes
9. keep the new eye-vs-non-eye blocker in `evaluation_only` status until it
   has been exercised on more real tester photos and public-backend runs

## Staged but not integrated anterior view router

- completed offline package:
  `anterior_view_router_v1_mobilenetv2_binary_colab_20260330_125330`
- shared package zip:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/packages/anterior_view_router_v1_mobilenetv2_binary_colab_20260330_125330_package.zip`
- current live behavior:
  the backend still uses the heuristic anterior view router
  `anterior_view_rules_v1` inside `_evaluate_anterior_view_type`
- trained router contract:
  route `iris_visible` if `p(iris_visible) >= 0.65`, route
  `eyelid_dominant` if `p(iris_visible) <= 0.35`, otherwise return
  `low_confidence_fallback`
- validation result:
  accuracy `0.9398`, AUC `0.9784`
- test result:
  accuracy `0.9502`, AUC `0.9717`
- eyelid-dominant class test result:
  precision `0.7838`, recall `0.7838`, F1 `0.7838`
- offline quick-check:
  sampled `12 / 12` iris_visible cases routed correctly and
  `11 / 12` sampled eyelid_dominant cases routed correctly, with `1 / 12`
  eyelid sample dropping into the intended low-confidence fallback
- current recommendation:
  keep the trained router offline/staged for now, then test it first on the
  local backend path against a small set of known eyelid, conjunctivitis,
  uveitis, and recapture examples before replacing the heuristic live route
