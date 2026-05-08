# Baseline 002 Run Summary

- Run type: evaluation-only baseline training
- Runtime device: `cpu`
- Torch version: `2.11.0+cpu`
- EfficientNetB0 initialization: `imagenet_pretrained`
- Warmup epochs: `4`
- Fine-tune epochs run: `10`
- Fine-tuned modules: `features[-2]`, `features[-1]`, and classifier
- Epochs run: `14`
- Best validation epoch: `9`
- Stop reason: `early_stopping_patience`
- Output folder: `F:\EyeScan_Local_Data\large_dr_82gb_work\fitting_v1_training_runs\baseline_002`

## Validation Metrics

- accuracy: `0.7071`
- macro F1: `0.7067`
- weighted F1: `0.7067`
- loss: `0.7233`

## Test Metrics

- accuracy: `0.7107`
- macro F1: `0.7078`
- weighted F1: `0.7078`
- loss: `0.7622`

## Baseline 001 Comparison

- validation macro F1 delta: `+0.0023`
- test macro F1 delta: `-0.0011`

## Class-Wise Test Metrics

- `normal_or_non_specific`: precision `0.8676`, recall `0.8429`, F1 `0.8551`, support `70`
- `dr_pattern_dominant`: precision `0.6186`, recall `0.8571`, F1 `0.7186`, support `70`
- `exudate_macular_pattern_dominant`: precision `0.7778`, recall `0.6000`, F1 `0.6774`, support `70`
- `mixed_hemorrhage_exudate_pattern`: precision `0.6230`, recall `0.5429`, F1 `0.5802`, support `70`

## Confusion Notes

- Class collapse observed: `false`
- Strong confusion pairs: `mixed_hemorrhage_exudate_pattern -> dr_pattern_dominant (22), exudate_macular_pattern_dominant -> mixed_hemorrhage_exudate_pattern (19), exudate_macular_pattern_dominant -> dr_pattern_dominant (8), normal_or_non_specific -> dr_pattern_dominant (7), mixed_hemorrhage_exudate_pattern -> exudate_macular_pattern_dominant (7)`

## Guardrails

- No app/backend/runtime integration was performed.
- No TFLite export was created.
- No production claim or promotion is approved from this run.
- Raw images and model weights remain outside the repository.
