# Baseline 001 Run Summary

- Run type: evaluation-only baseline training
- Runtime device: `cpu`
- Torch version: `2.11.0+cpu`
- EfficientNetB0 initialization: `imagenet_pretrained`
- Feature extractor frozen: `true`
- Epochs run: `14`
- Best validation epoch: `9`
- Stop reason: `early_stopping_patience`
- Output folder: `F:\EyeScan_Local_Data\large_dr_82gb_work\fitting_v1_training_runs\baseline_001`

## Validation Metrics

- accuracy: `0.7071`
- macro F1: `0.7043`
- weighted F1: `0.7043`
- loss: `0.7307`

## Test Metrics

- accuracy: `0.7143`
- macro F1: `0.7089`
- weighted F1: `0.7089`
- loss: `0.7737`

## Class-Wise Test Metrics

- `normal_or_non_specific`: precision `0.7875`, recall `0.9000`, F1 `0.8400`, support `70`
- `dr_pattern_dominant`: precision `0.6786`, recall `0.8143`, F1 `0.7403`, support `70`
- `exudate_macular_pattern_dominant`: precision `0.8125`, recall `0.5571`, F1 `0.6610`, support `70`
- `mixed_hemorrhage_exudate_pattern`: precision `0.6029`, recall `0.5857`, F1 `0.5942`, support `70`

## Confusion Notes

- Class collapse observed: `false`
- Strong confusion pairs: `exudate_macular_pattern_dominant -> mixed_hemorrhage_exudate_pattern (20), mixed_hemorrhage_exudate_pattern -> dr_pattern_dominant (18), dr_pattern_dominant -> normal_or_non_specific (7), mixed_hemorrhage_exudate_pattern -> exudate_macular_pattern_dominant (7), exudate_macular_pattern_dominant -> normal_or_non_specific (6)`

## Guardrails

- No app/backend/runtime integration was performed.
- No TFLite export was created.
- No production claim or promotion is approved from this run.
- Raw images and model weights remain outside the repository.
