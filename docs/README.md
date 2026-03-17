# EyeScan App Handoff

Last updated: 2026-03-16 22:55 Australia/Melbourne

## Purpose

This folder is the shared handoff pack after:

- integrating the Dell-trained anterior screening models into the Mac app-local backend
- testing the updated iPhone flow
- reviewing the latest exported PDFs and saved results

## Current product truth

- The live iPhone app is no longer quality-only.
- The current app-local backend now runs an evaluation-only anterior screening pipeline:
  1. `anterior_quality_gate_v1`
  2. `anterior_surface_binary_v2_simplecnn`
  3. `anterior_cataract_vs_normal_v1_simplecnn` only after `normal_surface`
- The app, saved history, and PDF exports can now show:
  - `Possible cataract pattern detected`
  - `Surface abnormality pattern detected`
  - `No screen-positive finding`
  - `Image quality needs recapture`
- The pipeline is still evaluation-only and must not be described as a medical diagnosis.

## Important finding from PDF review

The latest iPhone export set contained a mix of:

- real backend results from `SCREENING_PIPELINE`
- simulated results from `TEST_MODE`

This is why some PDFs looked useful and others looked vague or generic.

## Main recommendations

1. Turn `TEST_MODE` off before collecting screenshots, PDFs, or user evidence.
2. Clear old saved results before a fresh validation round, so multi-result PDFs are not mixed.
3. Keep `surface_abnormality` wording honest: it is a broad screen-positive gate, not a condition diagnosis.
4. Replace the broad surface-positive branch with narrower specialists such as:
   - conjunctivitis vs normal
   - pterygium vs normal
   - uveitis vs normal
   - eyelid abnormality vs normal
5. Keep glaucoma work separate for now, because it belongs to the fundus branch rather than the current anterior app flow.

## Related docs

- `PLAY_MONETIZATION_PLAN.md`
