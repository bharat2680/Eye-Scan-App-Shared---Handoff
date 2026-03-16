# Export Review Notes

Last updated: 2026-03-16 22:55 Australia/Melbourne

## Main finding

The latest iPhone export batch was mixed.

Saved result count reviewed:

- total results: `15`
- real backend results: `8`
- `TEST_MODE` results: `7`

## What this means

### Real backend results

These used:

- mode:
  `SCREENING_PIPELINE`
- model version:
  `anterior_screening_eval_v1`

Examples seen:

- `Possible cataract pattern detected`
- `Surface abnormality pattern detected`
- `Image quality needs recapture`

### Simulated results

These used:

- mode:
  `TEST_MODE`
- model version:
  `quality-gate-v1`

These are the main reason some exported PDFs looked vague or generic.

## Recommended process before next PDF evidence run

1. turn `TEST_MODE` off
2. clear old saved results
3. run a fresh short batch using only the live backend
4. export individual and multi-result PDFs again

