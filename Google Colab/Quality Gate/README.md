# Google Colab Quality Gate

This folder contains the Colab-side assets for the VisionFM external-eye
quality-gate experiment.

Files:

- `anterior_quality_gate_v3_visionfm_external_linearprobe.ipynb`
- `teyeds_quality_gate_v1.zip`

What still needs to stay on Google Drive:

- `MyDrive/Datasets/VFM Datasets/VFM_External_weights.pth`
- output folder:
  `MyDrive/EyeScan_Models/VisionFM_Quality_Gate_V3/`

Recommended Colab setup:

1. Open the notebook from GitHub or Drive.
2. Make sure the VisionFM external-eye weight file exists on Drive.
3. Upload or copy `teyeds_quality_gate_v1.zip` to `MyDrive/Datasets/` if the
   notebook does not fetch it from GitHub first.
4. Run on T4 GPU when available; the notebook falls back to CPU if needed.
