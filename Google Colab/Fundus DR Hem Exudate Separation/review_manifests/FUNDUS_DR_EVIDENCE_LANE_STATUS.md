# Fundus DR Evidence Lane Status

This document records the current status of the Fundus DR evidence and
evaluation lane as of the canonical checkpoint that includes
`challenge_manifest_v1.csv`.

## Current Canonical Manifests

`reviewed_manifest_v1.csv`

- row count: 2955
- purpose: canonical reviewed evidence pool used to preserve manually reviewed
  evidence decisions and provenance

`fitting_manifest_v1.csv`

- row count: 1864
- purpose: first fitting/training-preparation manifest used for Baselines 001
  and 002

`fitting_manifest_v2.csv`

- row count: 1696
- purpose: corrected and balanced fitting/training-preparation manifest derived
  after Round 1 error-slice review; used for Baseline 003 v2

`challenge_manifest_v1.csv`

- row count: 73
- purpose: independent evaluation/stress-test manifest derived from approved
  difficult/error-slice rows

## Manifest Separation

The lane is now separated into three distinct roles:

- reviewed evidence pool:
  `reviewed_manifest_v1.csv` holds the canonical reviewed evidence inventory
- fitting/training-preparation manifests:
  `fitting_manifest_v1.csv` and `fitting_manifest_v2.csv` define curated
  fitting sets for evaluation-only model training
- independent challenge/evaluation manifest:
  `challenge_manifest_v1.csv` defines a stress-test set for difficult,
  ambiguous, and quality-sensitive cases

`challenge_manifest_v1.csv` has zero evidence-ID overlap with
`fitting_manifest_v2.csv`, so the challenge set is independent from the current
v2 fitting manifest.

## Training and Evaluation Summary

Baseline 001

- manifest: `fitting_manifest_v1.csv`
- setup: EfficientNetB0, ImageNet initialization, frozen backbone
- result: reference baseline
- test macro F1: 0.7089

Baseline 002

- manifest: `fitting_manifest_v1.csv`
- setup: EfficientNetB0 warmup plus top-block fine-tuning
- result: no material improvement over Baseline 001
- test macro F1: 0.7078

Baseline 003 v2

- manifest: `fitting_manifest_v2.csv`
- setup: EfficientNetB0, frozen backbone
- result: underperformed and was timeout-limited
- test macro F1: 0.6528

No production model has been selected. No model has been promoted. No
app/backend integration is approved.

## Round 1 Error-Slice Review Summary

Round 1 review showed that `mixed_hemorrhage_exudate_pattern` was too broad and
often overlapped visually with `dr_pattern_dominant` or
`exudate_macular_pattern_dominant`.

As a result:

- many ambiguous rows were corrected, held out, or excluded during
  `fitting_manifest_v2.csv` construction
- the challenge set was derived from difficult rows, second-review cases,
  label-boundary candidates, and quality stress cases
- the canonical challenge manifest is intentionally smaller but cleaner and
  independent from the current v2 fitting manifest

## Current Recommendation

Do not run a blind Baseline 004 yet.

Do not:

- promote any model
- integrate any model into app/backend/runtime
- export TFLite
- make production claims

Next safe lane:

- challenge evaluation planning against `challenge_manifest_v1.csv`
- additional manual review of difficult or ambiguous cases
- data expansion before more training, if broader coverage is needed

## Safety Statement

- no TFLite export is approved
- no app/backend/runtime changes are approved from this lane status
- no production claims are approved
- all model artifacts remain evaluation-only and outside the repo
- challenge rows must not be used for training
