# Anterior Bakeoff 2026-03-28

## Scope

Quick backend bakeoff against representative images from the current anterior
dataset folders:

- `Normal`
- `Conjunctivitis`
- `Uveitis`
- `Pterygium`
- `Cataract`
- `Eyelid`

This was a lightweight reliability check, not a formal fairness evaluation.
The dataset used here does not include robust demographic labels, so this
cannot prove race/region parity by itself.

## What was tested

Three representative images were sampled from each folder and sent through the
current local backend endpoint:

- `POST /v1/predict`
- backend state under test: `anterior_screening_eval_v8`

## Main findings

### 1. Non-eye filtering is no longer the main problem

The pre-pipeline `eye_vs_non_eye_gate_v1_simplecnn` blocker is doing useful
work. Obvious non-eye images are now reliably stopped before they enter the
anterior specialist router.

### 2. The current bottleneck is specialist overlap

The remaining major issue is entanglement across the surface specialists:

- `conjunctivitis`
- `uveitis`
- `pterygium`
- `eyelid_abnormality`

In multiple tested red-eye / surface-positive samples, several specialists
scored strongly at once instead of separating cleanly.

That means the system often has to degrade to a broader fallback such as:

- `Surface abnormality pattern detected`

instead of naming a more specific condition confidently.

### 3. The ambiguity guardrail is helping

This is still better than the earlier behavior where the pipeline overcalled
`Possible conjunctivitis pattern detected` too often.

The newer routing logic is now correctly refusing to over-promote a specific
specialist when several surface models fire too closely together.

### 4. Some "normal" images were not useful as app-style benchmarks

Several tested `Normal` samples were tiny cropped images and were blocked by
the quality gate as:

- `Image quality needs recapture`
- `image_too_small`

That is not necessarily a model failure. It mostly means those dataset samples
do not match the framing/style of real EyeScan captures.

## Representative observations

### Conjunctivitis example

At least one conjunctivitis-labeled sample did not resolve to a clean
conjunctivitis result. Instead, multiple surface specialists fired strongly,
which caused a broader `surface_abnormal` style outcome.

### Pterygium example

At least one pterygium-labeled sample also triggered strong scores across
multiple specialists at once:

- conjunctivitis
- uveitis
- pterygium
- eyelid abnormality

This confirms that the main issue is poor separation between surface-positive
specialists, not just missing model coverage.

### Quality rejection example

At least one surface-positive sample was stopped earlier by the quality gate,
showing that quality-stage gating is still affecting evaluation outcomes for
some real disease images.

## What this bakeoff does NOT prove

- It does **not** prove fairness across races or regions.
- It does **not** prove the app is ready for clinical-style anterior
  subclassing.
- It does **not** mean the eyelid or uveitis models are absent.

What it does prove is that the current surface specialists are still too
correlated on many inflamed / eyelid / red-eye examples.

## Practical interpretation

Current state:

- non-eye rejection: materially improved
- broad surface-positive detection: usable
- precise separation between conjunctivitis / uveitis / pterygium / eyelid:
  still not trustworthy enough

## Recommended next steps

1. Keep the ambiguity fallback.

Do not force a specific anterior label when multiple surface specialists are
clustered tightly.

2. Build a small real EyeScan evaluation pack.

Use real phone captures from actual EyeScan-style framing for:

- normal
- conjunctivitis
- uveitis
- pterygium
- eyelid dermatitis / blepharitis / eczema style cases
- non-eye negatives

3. Improve specialist separation instead of only adding more models.

Best candidate approaches:

- retrain the eyelid-vs-conjunctivitis boundary with stronger eyelid data
- calibrate the four surface specialists jointly
- or add a second-stage surface ranker / calibrator on top of current outputs

4. Do not treat this as a fairness signoff.

If parity across races / regions / eye shapes is a real product requirement,
that needs a deliberately curated and labeled evaluation set, not just a mixed
folder bakeoff.

## Release implication

For the app right now, the safest stance is:

- keep the current anterior pipeline
- keep non-eye blocking
- allow broad `surface abnormality` fallbacks
- continue refining specialist separation before claiming precise anterior
  subclass reliability
