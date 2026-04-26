# Google Colab Fundus Glaucoma PAPILA

This folder contains the Colab-side assets for a stronger GPU-backed `PAPILA`
glaucoma training run.

Files:

- `train_fundus_glaucoma_papila_v3_officialfold_colab.py`
- `fundus_glaucoma_papila_v3_efficientnetb2_officialfold_colab.ipynb`

Accepted dataset input on Google Drive:

- preferred raw archive:
  `MyDrive/Datasets/PAPILA.zip`
- fallback:
  no Drive upload required; the notebook can download the latest public
  `PAPILA` zip from Figshare directly into the Colab runtime

Recommended notebook now:

- `fundus_glaucoma_papila_v3_efficientnetb2_officialfold_colab.ipynb`

Why this `v3` recipe is stronger than the earlier local PAPILA baselines:

- uses the official `HelpCode/kfold/Test 2` binary healthy-vs-glaucoma folds
- keeps both eyes of the same patient on the same side of the split
- excludes `suspicious` the same way the paper's binary setup does
- uses a stronger `EfficientNetB2` transfer-learning backbone
- uses a balanced `50 / 50` repeated sampler for the imbalanced glaucoma class
- keeps preprocessing app-friendly with plain `resize_with_pad`

What the notebook does:

1. mounts Google Drive
2. uses `MyDrive/Datasets/PAPILA.zip` if present
3. otherwise downloads the latest public `PAPILA` zip from Figshare into
   Colab
4. extracts only the fundus images, clinical spreadsheets, and official binary
   fold files into the Colab workdir
5. rebuilds a binary `Healthy` vs `Glaucoma` dataset from the official fold
   membership
6. creates a deterministic patient-level validation split from the official
   training fold
7. trains a stronger transfer-learning classifier on GPU if available
8. sanitizes the exported `.keras` archive for better backend compatibility
9. saves artifacts to Drive

Expected output files on Drive:

- `best_model.keras`
- `metrics.json`
- `label_map.json`
- `inference_contract.json`
- `train_history.json`
- `train_config.json`

Output location:

- `MyDrive/EyeScan_Models/Fundus_Glaucoma_PAPILA_V3/`

Recommended Colab setup:

1. Either keep `PAPILA.zip` in `MyDrive/Datasets/` or let the notebook fetch it
   from Figshare automatically.
2. Upload only `fundus_glaucoma_papila_v3_efficientnetb2_officialfold_colab.ipynb`
   to Drive or open it directly in Colab.
3. In Colab, switch runtime to `T4 GPU` if available.
4. Run the notebook from top to bottom.

Notes:

- the Nature paper shows an author correction dated `2024-04-17`; for this
  training path, that correction is treated as publication metadata /
  acknowledgement cleanup rather than a label or split change
- the paper's published baseline uses expert-guided optic-disc ROI crops, but
  this Colab recipe intentionally trains on full fundus images so the resulting
  model can stay compatible with future app/backend packaging
- if this full-image run is still weak, the next stronger evaluation-only step
  would be a contour-guided ROI experiment rather than another simple full-image
  rerun
