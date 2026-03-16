# Codex Handoff

Last updated: 2026-03-16 22:55 Australia/Melbourne

## Shared goal

Move EyeScan from honest evaluation screening toward diagnosis-like outputs without making claims the models do not support.

## What the Mac side has already done

- replaced the old quality-only stub backend
- integrated:
  - `anterior_quality_gate_v1`
  - `anterior_surface_binary_v2_simplecnn`
  - `anterior_cataract_vs_normal_v1_simplecnn`
- updated the iPhone result screen, history, and PDF exports

## What the Dell side should assume now

- the current app can consume real anterior screening results
- cataract is already supported as an evaluation-only diagnosis-like label
- surface-positive outputs are still broad and are the next bottleneck

## Most useful next Dell deliverables

1. narrow surface specialists
2. packaging notes with metrics and preprocessing contracts
3. clean deployment recommendation for each artifact

## Important caution

Do not judge the latest PDF batch without separating:

- `SCREENING_PIPELINE` results
- `TEST_MODE` results

The last reviewed export set contained both.

