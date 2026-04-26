# Anterior View Router V1 Binary Review

## Run

- model:
  `anterior_view_router_v1_mobilenetv2_binary_colab_20260330_125330`
- package zip:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/packages/anterior_view_router_v1_mobilenetv2_binary_colab_20260330_125330_package.zip`
- extracted artifact:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/artifacts/anterior/anterior_view_router_v1_mobilenetv2_binary_colab_download/anterior_view_router_v1_mobilenetv2_binary_colab_20260330_125330_package`
- source-of-truth labels:
  `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/datasets/anterior/view_router/labels_reviewed_final.csv`

## Core Result

- trainable classes:
  `eyelid_dominant`, `iris_visible`
- runtime fallback:
  do not train `unclear`; instead use threshold-based fallback
- test metrics:
  accuracy `0.9502`, AUC `0.9717`
- eyelid-dominant class metrics:
  precision `0.7838`, recall `0.7838`, F1 `0.7838`
- confusion matrix:
  `[[29, 8], [8, 276]]`

## Local Offline Quick-Check

Quick-check artifact:
- `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/artifacts/anterior/anterior_view_router_v1_mobilenetv2_binary_colab_download/offline_quickcheck.json`

Sampling rule:
- `12` random included `eyelid_dominant` rows
- `12` random included `iris_visible` rows
- runtime decision thresholds from the package contract:
  - iris route if `p(iris_visible) >= 0.65`
  - eyelid route if `p(iris_visible) <= 0.35`
  - otherwise `low_confidence_fallback`

Observed summary:
- `iris_visible`: `12 / 12` hard-routed correctly
- `eyelid_dominant`: `11 / 12` hard-routed correctly
- `eyelid_dominant`: `1 / 12` fell into `low_confidence_fallback`
- no sampled eyelid-dominant case was hard-misrouted to iris-visible
- no sampled iris-visible case was hard-misrouted to eyelid-dominant

Notable sampled fallback:
- `Eyelid/312.jpeg`
  `p(iris_visible) = 0.5763`
  fallback was appropriate because the model stayed between the two confident
  routing thresholds

## Local Backend-Only Regression Pass

Regression artifact:
- `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/artifacts/anterior/anterior_view_router_v1_mobilenetv2_binary_colab_download/local_backend_router_regression.json`

Comparison setup:
- current backend heuristic router:
  `anterior_view_rules_v1`
- trained router package:
  `anterior_view_router_v1_mobilenetv2_binary_colab_20260330_125330`
- evaluation set:
  all `2,042` included reviewed router-label rows
  (`1,799` `iris_visible`, `243` `eyelid_dominant`)
- trained-router runtime thresholds:
  `iris_visible` if `p(iris_visible) >= 0.65`,
  `eyelid_dominant` if `p(iris_visible) <= 0.35`,
  else `low_confidence_fallback`

Observed totals:
- heuristic router:
  `1,577 / 2,042` correct, `381` hard misroutes, `84` unclear/fallback
- trained router:
  `1,923 / 2,042` correct, `55` hard misroutes, `64` fallback

Interpretation:
- the trained router is a clear improvement over the current heuristic route on
  the reviewed router source-of-truth set
- the biggest win is on eyelid-dominant cases that the heuristic route often
  over-promotes to `iris_visible`
- the trained router still has some borderline eyelid-folder images that fall
  into either `low_confidence_fallback` or occasional `eyelid_dominant`
  overcalls, so a small real EyeScan photo pass is still recommended before a
  live swap

## Packaging Check

Verified package contents:
- `best_model.keras`
- `metrics.json`
- `confusion_matrix.json`
- `confusion_matrix.png`
- `label_map.json`
- `train_config.json`
- `inference_contract.json`
- `HANDOFF.md`
- `train_history.json`

Packaging note:
- the original Desktop export was missing `train_history.json` inside the zip
- the package zip in the shared repo was rebuilt so it now matches the handoff
  contents cleanly

## Decision

- status:
  `accepted_for_offline_handoff`
- recommendation:
  this is good enough to preserve as the first successful trained anterior
  view-router package
- current limitation:
  the live backend still uses the heuristic `anterior_view_rules_v1` router, so
  this package should remain offline/staged until a small real-photo regression
  pass is completed on the local backend path
