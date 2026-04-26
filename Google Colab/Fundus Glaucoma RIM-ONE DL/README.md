# Google Colab Fundus Glaucoma RIM-ONE DL

This folder contains the Colab-side assets for a stronger glaucoma training run
using the official `RIM-ONE DL` dataset.

Files:

- `train_fundus_glaucoma_rimone_v1_vgg19_byhospital_colab.py`
- `fundus_glaucoma_rimone_v1_vgg19_byhospital_colab.ipynb`

Dataset source order:

- preferred optional Drive upload:
  `MyDrive/Datasets/rim-one-dl-images.zip`
- fallback:
  the notebook can download the official image archive directly from the
  `RIM-ONE DL` repository entry link

Recommended notebook:

- `fundus_glaucoma_rimone_v1_vgg19_byhospital_colab.ipynb`

Why this bundle exists:

- `REFUGE` is still access-gated
- `PAPILA` improved on GPU but still did not clearly beat the current
  `Eye-Fundus` fallback glaucoma model
- `RIM-ONE DL` is an official public glaucoma dataset with published train/test
  partitions and published CNN baselines

Default protocol in this bundle:

- uses the official `by_hospital` split by default rather than the easier random
  split
- creates a deterministic validation split only inside the official training
  portion
- trains a `VGG19` transfer-learning classifier because the official benchmark
  reports strong performance for `VGG19` on `RIM-ONE DL`

What the notebook does:

1. mounts Google Drive
2. checks for an existing `RIM-ONE DL` image zip in Drive
3. otherwise downloads the official images zip via the repository's public
   download link
4. extracts the archive and rebuilds a standard `train / valid / test` binary
   layout for the selected partition variant
5. trains a `VGG19` image classifier on GPU if available
6. sanitizes the exported `.keras` archive for better downstream compatibility
7. saves artifacts to:
   `MyDrive/EyeScan_Models/Fundus_Glaucoma_RIM_ONE_DL_V1/`

Expected output files on Drive:

- `best_model.keras`
- `metrics.json`
- `label_map.json`
- `inference_contract.json`
- `train_history.json`
- `train_config.json`

Recommended Colab setup:

1. Upload only `fundus_glaucoma_rimone_v1_vgg19_byhospital_colab.ipynb` to
   Drive or open it directly in Colab.
2. Switch runtime to `T4 GPU` if available.
3. Run the notebook from top to bottom.

Notes:

- official repository:
  `https://github.com/miag-ull/rim-one-dl`
- official paper:
  `https://www.ias-iss.org/ojs/IAS/article/view/2346`
- official repository README says the image archive includes both the random and
  by-hospital variants; this bundle defaults to the harder by-hospital split
- if the by-hospital layout inside the downloaded archive differs from the
  expected naming conventions, the script prints layout debug information to
  make the next fix straightforward
