# Google Colab Fundus Glaucoma Chaksu

This folder contains the Colab-side assets for a stronger glaucoma training run
using the official `Chaksu IMAGE` dataset.

Files:

- `train_fundus_glaucoma_chaksu_v1_efficientnetb2_colab.py`
- `fundus_glaucoma_chaksu_v1_efficientnetb2_colab.ipynb`

Dataset source order:

- optional Drive upload:
  `MyDrive/Datasets/Chaksu.zip`
- fallback:
  the notebook can download the latest public `Chaksu` archive directly from
  Figshare

Why this bundle exists:

- `REFUGE` is still access-gated
- `PAPILA` improved on GPU but still did not clearly beat the current
  `Eye-Fundus` fallback glaucoma model
- `RIM-ONE DL` direct-download run worked but underperformed badly
- `Chaksu` is larger, public, glaucoma-specific, and already has an official
  train/test split

What the notebook does:

1. mounts Google Drive
2. checks for an existing Chaksu zip in Drive
3. otherwise downloads the latest public archive from Figshare
4. extracts only the original fundus images and glaucoma-decision tables
5. rebuilds a binary `Healthy` vs `Glaucoma` dataset using the official
   train/test split and the majority-vote glaucoma decision material
6. creates a deterministic validation split inside the official training split
7. trains an `EfficientNetB2` classifier on GPU if available
8. sanitizes the exported `.keras` archive for better downstream compatibility
9. saves artifacts to:
   `MyDrive/EyeScan_Models/Fundus_Glaucoma_Chaksu_V1/`

Expected output files on Drive:

- `best_model.keras`
- `metrics.json`
- `label_map.json`
- `inference_contract.json`
- `train_history.json`
- `train_config.json`

Recommended Colab setup:

1. Upload only `fundus_glaucoma_chaksu_v1_efficientnetb2_colab.ipynb` to Drive
   or open it directly in Colab.
2. Switch runtime to `T4 GPU` if available.
3. Run the notebook from top to bottom.

Notes:

- official paper:
  `https://www.nature.com/articles/s41597-023-01943-4`
- official Figshare:
  `https://figshare.com/articles/dataset/Ch_k_u_A_glaucoma_specific_fundus_image_database/20123135`
- Figshare currently lists the public archive as roughly `10.56 GB`, so the
  direct Colab download can take meaningfully longer than `PAPILA` or
  `RIM-ONE DL`
- the Scientific Data article shows an author correction published on
  `2023-04-06`; this recipe assumes the official split and majority-vote
  semantics remain valid for image-only training
