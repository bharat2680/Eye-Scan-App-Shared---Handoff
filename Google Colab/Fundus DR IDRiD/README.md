# Google Colab Fundus DR IDRiD

This folder contains the Colab-side assets for GPU-backed `IDRiD`
diabetic-retinopathy-vs-healthy training runs.

Files:

- `train_fundus_dr_idrid_colab.py`
- `fundus_dr_idrid_v2_efficientnetb0_colab.ipynb`
- `train_fundus_dr_idrid_v3_balanced_colab.py`
- `fundus_dr_idrid_v3_efficientnetb2_balanced_colab.ipynb`

Required dataset input on Google Drive:

- preferred raw archive:
  `MyDrive/Datasets/B. Disease Grading.zip`

Recommended notebook now:

- `fundus_dr_idrid_v3_efficientnetb2_balanced_colab.ipynb`

Why `v3` is stronger:

- larger `EfficientNetB2` backbone
- `260 x 260` input size
- balanced `50 / 50` repeated training sampler
- longer staged fine-tuning
- `resize_with_pad` preprocessing to preserve the retinal field better

What the notebook does:

1. mounts Google Drive
2. reads the raw `IDRiD` grading archive from Drive
3. rebuilds a binary `Healthy` vs `Diabetic Retinopathy` dataset in Colab
4. preserves the official `test` split and creates a deterministic validation
   split from the official training set
5. trains a stronger transfer-learning classifier on GPU if available
6. sanitizes the exported `.keras` archive for better backend compatibility
7. saves artifacts to Drive

Expected output files on Drive:

- `best_model.keras`
- `metrics.json`
- `label_map.json`
- `inference_contract.json`
- `train_history.json`
- `train_config.json`

Output locations:

- `v2`: `MyDrive/EyeScan_Models/Fundus_DR_IDRiD_V2/`
- `v3`: `MyDrive/EyeScan_Models/Fundus_DR_IDRiD_V3/`

Recommended Colab setup:

1. Keep `B. Disease Grading.zip` in `MyDrive/Datasets/`.
2. Upload only `fundus_dr_idrid_v3_efficientnetb2_balanced_colab.ipynb` to
   Drive or open it directly in Colab.
3. In Colab, switch runtime to `T4 GPU` if available.
4. Run the notebook from top to bottom.

Notes:

- this workflow avoids making an extra local `IDRiD` zip on the MacBook
- the earlier `v2` Colab run completed successfully but underperformed the
  local `fundus_dr_idrid_v1_simplecnn` baseline
- `v3` is the next stronger rerun to try before promoting any new `IDRiD`
  artifact into packaging or backend integration
