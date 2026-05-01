# Raw Candidate Manifest Helper

This folder contains a helper for creating a raw candidate manifest for
`fundus_dr_hem_exudate_separation_v1`.

The generated CSV is not training-ready. It is a review queue only.

## Purpose

`build_raw_candidate_manifest.py` scans selected image folders and writes
candidate rows using the approved manifest schema.

It does not train, does not read or write model files, does not create model
artifacts, and does not move, copy, delete, or alter image files.

Every generated row has:

- `final_label` empty
- `review_status = unreviewed`
- `split = unset`
- `challenge_only = false`

`proposed_label` is only a hint. It may help queue candidates for review, but
future training export must use reviewed `final_label` only.

## Supported Images

The helper scans recursively for:

- `.jpg`
- `.jpeg`
- `.png`
- `.bmp`
- `.tif`
- `.tiff`
- `.webp`

Output rows are sorted deterministically by resolved image path.

## Example Commands

Dry run:

```bash
python3 "Google Colab/Fundus DR Hem Exudate Separation/tools/build_raw_candidate_manifest.py" \
  --source-dataset "Eye Disease Image Dataset" \
  --source-label "Diabetic Retinopathy" \
  --proposed-label dr_pattern_dominant \
  --dry-run \
  "/path/to/Diabetic Retinopathy"
```

Build a raw candidate manifest for a DR source folder:

```bash
python3 "Google Colab/Fundus DR Hem Exudate Separation/tools/build_raw_candidate_manifest.py" \
  --source-dataset "Eye Disease Image Dataset" \
  --source-label "Diabetic Retinopathy" \
  --proposed-label dr_pattern_dominant \
  --output raw_candidate_manifest.csv \
  "/path/to/Diabetic Retinopathy"
```

Build a raw candidate manifest for a normal source folder:

```bash
python3 "Google Colab/Fundus DR Hem Exudate Separation/tools/build_raw_candidate_manifest.py" \
  --source-dataset "Eye-Fundus" \
  --source-label "Healthy" \
  --proposed-label normal_or_non_specific \
  --output raw_candidate_manifest.csv \
  "/path/to/Healthy"
```

## Safety Notes

- Generated rows are not accepted rows.
- Generated rows are not fitting rows.
- `final_label` is intentionally empty.
- `proposed_label` must never be used as the training label.
- Manual image review is the next step, not training.
- Do not use the generated raw manifest directly for model fitting.
- Do not overwrite preserved baselines or package artifacts.
- Do not create `reviewed_manifest_v1.csv`, `fitting_manifest_v1.csv`, or
  `challenge_manifest_v1.csv` with this helper.

The script refuses package/model artifact-style output names such as:

- `model.tflite`
- `labels.txt`
- `fundus_broad_abnormality_v1_efficientnetb0_colab_package.zip`
- `anterior_boundary_v1_efficientnetb0_colab_package.zip`

It also refuses overwrite unless `--overwrite` is explicitly passed.
