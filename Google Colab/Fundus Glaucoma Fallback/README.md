# Google Colab Fundus Glaucoma Fallback

This folder contains the Colab-side assets for a stronger GPU-backed fallback
glaucoma training run using the `Eye-Fundus` archive.

Files:

- `eye_fundus_glaucoma_vs_healthy.zip`
- `train_fundus_glaucoma_eyefundus_colab.py`
- `fundus_glaucoma_eyefundus_v3_efficientnetb0_colab.ipynb`

Accepted dataset inputs on Google Drive:

- preferred filtered upload:
  `MyDrive/Datasets/eye_fundus_glaucoma_vs_healthy.zip`
- fallback raw archive:
  `MyDrive/Datasets/Eye-Fundus.zip`

The bundled filtered zip is about `36 MB`, so it is the easier upload target.

What the notebook does:

1. mounts Google Drive
2. checks for the preferred filtered zip first
3. falls back to the raw `Eye-Fundus.zip` archive if needed
4. extracts a `Healthy` vs `Glaucoma` dataset into the Colab workdir
5. trains an `EfficientNetB0` transfer-learning classifier on GPU if available
6. saves artifacts back to:
   `MyDrive/EyeScan_Models/Fundus_Glaucoma_EyeFundus_V3/`

Expected output files on Drive:

- `best_model.keras`
- `metrics.json`
- `label_map.json`
- `inference_contract.json`
- `train_history.json`
- `train_config.json`

Recommended Colab setup:

1. Put either `eye_fundus_glaucoma_vs_healthy.zip` or `Eye-Fundus.zip` into
   `MyDrive/Datasets/`.
2. Upload only `fundus_glaucoma_eyefundus_v3_efficientnetb0_colab.ipynb` to
   Drive or open it directly in Colab.
3. Open the notebook and switch runtime to `T4 GPU` if available.
4. Run the notebook from top to bottom.

Notes:

- the notebook keeps the original `train` / `valid` / `test` split when it
  builds from the raw `Eye-Fundus.zip` archive
- the notebook is now self-contained, so the separate
  `train_fundus_glaucoma_eyefundus_colab.py` file is optional reference rather
  than a required upload
- this is intended to beat the CPU-only Mac baseline
  `fundus_glaucoma_eyefundus_v1_simplecnn`, not to replace the official
  specialist-data plan built around `REFUGE` / `PAPILA`
