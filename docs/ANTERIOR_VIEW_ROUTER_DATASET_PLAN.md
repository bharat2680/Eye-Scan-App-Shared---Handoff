# Anterior View Router Dataset Plan

Date: 2026-03-29

## Goal

Prepare a lightweight multiclass dataset for a **view router**, not a disease classifier.

Target router labels:

- `iris_visible`
- `eyelid_dominant`
- `unclear`

This router is intended to sit between:

- quality gate
- eye / non-eye gate
- anterior specialists

and decide whether an image should:

- continue into the normal anterior screening path
- go into an eyelid-limited path
- return recapture guidance

## Source dataset

Current source root:

`/Users/bharatsharma/Desktop/Image Dataset on Eye Diseases Classification (Uveitis, Conjunctivitis, Cataract, Eyelid) with Symptoms and SMOTE Validation`

Observed source classes:

- `Cataract`
- `Conjunctivitis`
- `Eyelid`
- `Normal`
- `Pterygium`
- `Uveitis`

Observed counts:

- Cataract: 544
- Conjunctivitis: 357
- Eyelid: 525
- Normal: 649
- Pterygium: 102
- Uveitis: 223

Important caveat:

- this source contains many baked-in synthetic / augmented files with `aug_` prefixes
- the router manifest builder excludes those by default

## Router labeling principles

The router label should describe **view type**, not disease.

### 1. `iris_visible`

Use when:

- the eye is clearly present
- the iris / pupil region is visible enough for broader anterior screening
- the framing is adequate for surface-style routing

Can include:

- normal eyes
- conjunctivitis-like eyes
- uveitis-like eyes
- pterygium-like eyes
- cataract-like eyes

as long as the **view type** is iris-visible.

### 2. `eyelid_dominant`

Use when:

- the image is still a valid eye-region image
- but the eyelid / lid-margin / surrounding skin dominates the frame
- and iris visibility is too limited for fair conjunctivitis / uveitis / pterygium routing

Can include:

- abnormal eyelids
- normal eyelids
- partial-eye captures

Do **not** use this label as shorthand for disease.

### 3. `unclear`

Use when:

- framing is too poor
- blur / glare / darkness dominates
- the image is ambiguous
- the image is not sufficiently trustworthy for either `iris_visible` or `eyelid_dominant`

This is the router’s safe fallback.

## Practical relabeling strategy

### Good first-pass heuristics by source folder

These are **seed suggestions only**. Human review is still required.

- `Normal`
  - usually seed to `iris_visible`
  - move borderline or partial-eye captures to `unclear`
- `Conjunctivitis`
  - usually seed to `iris_visible`
  - eyelid-heavy examples may move to `eyelid_dominant`
- `Uveitis`
  - usually seed to `iris_visible`
  - move poor framing to `unclear`
- `Pterygium`
  - usually seed to `iris_visible`
- `Cataract`
  - usually seed to `iris_visible`
- `Eyelid`
  - often seed to `eyelid_dominant`
  - but very clear iris-visible captures should be relabeled to `iris_visible`
  - poor or ambiguous examples should be `unclear`

## Dataset quality rules

### Exclude by default

- files whose basename starts with `aug_`
- duplicates
- corrupted files
- screenshots of app UI
- exports / PDFs / non-photographic assets

### Keep balanced

Target first-pass minimum:

- 500+ real images per router label

Better pilot target:

- 1,000+ real images per router label

### Diversity targets

Ensure coverage across:

- skin tones
- ages
- eye shapes
- lighting conditions
- phone cameras
- indoor / outdoor captures
- open-lid and closed-lid dominant views

## Manifest workflow

Use the shared labeling template:

`datasets/anterior/view_router/labels_template.csv`

Then build the manifest with:

```bash
python3 /Users/bharatsharma/Documents/Playground/EyeScan_Shared/scripts/build_view_router_manifest.py \
  --spec /Users/bharatsharma/Documents/Playground/EyeScan_Shared/configs/anterior_view_router_v1_dataset_spec.json
```

Output manifest:

`/Users/bharatsharma/Documents/Playground/EyeScan_Shared/datasets/anterior/view_router/anterior_view_router_v1_manifest.jsonl`

## Manifest record format

Each JSONL row should contain:

```json
{
  "path": "/absolute/path/to/image.jpg",
  "relative_path": "Eyelid/373.jpeg",
  "source_class": "Eyelid",
  "router_label": "eyelid_dominant",
  "split": "train"
}
```

## Evaluation target for the future router model

Primary metrics:

- macro F1
- per-class precision / recall
- confusion matrix

Safety goals:

- eyelid_dominant recall >= 0.95
- unclear recall >= 0.90
- eyelid_dominant misrouted to iris_visible < 2%

## Non-goals

This router should **not**:

- diagnose eyelid disease
- replace the quality gate
- replace the eye / non-eye gate
- use disease labels as its training target

## Recommended next step

1. Fill the CSV with human-reviewed router labels
2. Build the JSONL manifest
3. Audit final counts per label and per split
4. Only then design / run the lightweight multiclass router training
