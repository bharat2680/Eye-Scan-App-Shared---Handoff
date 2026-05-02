# Batch 008 Kaggle DR 224 Full Upload Pack

## Purpose

This is a ChatGPT visual review upload package for the EyeScan fundus DR evidence lane.
It includes the actual individual PNG image files so each image can be inspected separately.
Contact sheets are included only as optional navigation aids.

Source archive:

- `/Users/bharatsharma/Desktop/Datasets/Diabetic Retinopathy/archive.zip`

Included source classes:

| Source class | Images | Optional contact-sheet pages |
| --- | ---: | ---: |
| `Moderate` | 999 | 63 |
| `Severe` | 193 | 13 |
| `Proliferate_DR` | 295 | 19 |
| **Total** | **1487** | **95** |

Excluded source classes:

- `No_DR`
- `Mild`

## Files

- `images/moderate/`: copied original 224x224 Moderate PNG images
- `images/severe/`: copied original 224x224 Severe PNG images
- `images/proliferate_dr/`: copied original 224x224 Proliferate_DR PNG images
- `batch_008_full_index.csv`: master upload/review index
- `optional_contact_sheets/`: 4x4 navigation contact sheets
- `chatgpt_handoff/`: ChatGPT-generated review-support files, including an
  enriched index, priority review order, and integration note
- `chatgpt_candidate_findings/`: second ChatGPT handoff with AI-assisted
  candidate triage, shortlist CSV, summary, prompt handoff, and candidate
  contact sheets

The individual image files are the primary review material. The optional contact sheets are for navigation only.

## Review Status

This is a visual review pack only.

Source labels are not accepted labels. They are source metadata only and must not be treated as ground truth for EyeScan review buckets.

The blank review columns in `batch_008_full_index.csv` are intentionally empty:

- `proposed_review_bucket`
- `reviewer_decision`
- `notes`

This pack must be visually reviewed before any training or integration lane is created.

The `chatgpt_handoff/` files are review-support material only. Any `auto_*`
values are automated quality-triage helpers, not diagnostic labels, accepted
evidence labels, or training labels.

The `chatgpt_candidate_findings/` files are candidate triage only. The
`chatgpt_candidate_review_bucket` values are not accepted labels and must be
manually confirmed before any row can enter reviewed evidence.

## Safety Notes

- No rows were added to `reviewed_manifest_v1.csv`.
- No rows were added to `fitting_manifest_v1.csv`.
- No rows were added to `challenge_manifest_v1.csv`.
- No accepted evidence rows were created.
- No training was performed.
- No integration was performed.
- No model changes were made.
- No app, backend, runtime, or model-loading changes were made.
- No preserved package changes were made.

## Intended Manual Review Buckets

Use these buckets during visual review when assigning review outcomes:

- `dr_pattern_dominant`
- `exudate_macular_pattern_dominant`
- `mixed_hemorrhage_exudate_pattern`
- `hemorrhage_pattern_dominant_non_dr`
- `normal_or_non_specific`
- `needs_second_review`
- `unusable_low_quality`
