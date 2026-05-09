# Baseline 003 v2 Run Summary

## Scope

Baseline 003 v2 is an evaluation-only run using canonical `fitting_manifest_v2.csv` and the Windows resolved manifest.
It does not integrate into app/backend/runtime, export TFLite, promote a model, or make production claims.

## Setup

- Model: EfficientNetB0
- Initialization: ImageNet-pretrained checkpoint from this run loaded for final evaluation
- Backbone: frozen
- Training: classifier head only
- Top-block fine-tuning: not used
- Input size: 224x224
- Device: cpu
- Epochs run: 5
- Best validation epoch: 3
- Stop reason: stopped_execution_timeout_after_epoch_5

## Validation Metrics

- Accuracy: 0.7031
- Macro F1: 0.7054
- Weighted F1: 0.7054
- Loss: 0.8549

## Test Metrics

- Accuracy: 0.6523
- Macro F1: 0.6528
- Weighted F1: 0.6528
- Loss: 0.8644

## Comparison Against Baselines 001/002

- Baseline 001 test macro F1: 0.7089
- Baseline 002 test macro F1: 0.7078
- Baseline 003 v2 test macro F1: 0.6528
- Delta vs Baseline 001 test macro F1: -0.0561
- Delta vs Baseline 002 test macro F1: -0.0550

## Strongest Test Confusions

- `exudate_macular_pattern_dominant` -> `mixed_hemorrhage_exudate_pattern`: 16
- `mixed_hemorrhage_exudate_pattern` -> `dr_pattern_dominant`: 15
- `normal_or_non_specific` -> `dr_pattern_dominant`: 12
- `mixed_hemorrhage_exudate_pattern` -> `exudate_macular_pattern_dominant`: 10
- `normal_or_non_specific` -> `mixed_hemorrhage_exudate_pattern`: 7
- `dr_pattern_dominant` -> `mixed_hemorrhage_exudate_pattern`: 7
- `exudate_macular_pattern_dominant` -> `dr_pattern_dominant`: 7
- `normal_or_non_specific` -> `exudate_macular_pattern_dominant`: 5

## Class Collapse Check

- Class collapse observed: no

## Per-Row Predictions

- Exported externally: `F:\EyeScan_Local_Data\large_dr_82gb_work\fitting_v1_training_runs\baseline_003_v2\baseline_003_v2_per_row_predictions_val_test.csv`
- Val/test prediction rows: 512

## Guardrails

- No app/backend/runtime integration.
- No TFLite export.
- No model promotion.
- No production claims.
- No canonical manifest changes.
- No raw images or model weights committed to repo.