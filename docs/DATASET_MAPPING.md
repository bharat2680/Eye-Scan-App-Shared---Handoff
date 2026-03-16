# Dataset Mapping

Last updated: 2026-03-17 00:07 Australia/Sydney

## Current known dataset references

### Dell-side references

- `F:\datasets\Image Dataset on Eye Diseases Classification.zip`
- `F:\datasets\Mendeley Dataset\Original Dataset.zip`
- `F:\datasets\TEyeDSComplete`
- `F:\datasets\EyeScan_Anterior_Images\Real_Extracted_Images`

### User-mentioned external-drive reference

- `F:\My Passports\Datasets`

## Recommended current EyeScan role by source

### `Image Dataset on Eye Diseases Classification.zip`

Use for:

- anterior surface routing bootstrap
- cataract-vs-normal specialist
- future narrower surface specialists

Available label family:

- cataract
- conjunctivitis
- eyelid
- normal
- pterygium
- uveitis

## Task-specific anterior views now prepared

### `anterior_conjunctivitis_vs_normal_v1`

- positive:
  `conjunctivitis`
- negative:
  `normal`
- counts:
  train `249 / 455`
  val `54 / 97`
  test `54 / 97`
- current role:
  best next surface-specific bootstrap specialist

### `anterior_uveitis_vs_normal_v1`

- positive:
  `uveitis`
- negative:
  `normal`
- counts:
  train `157 / 455`
  val `33 / 97`
  test `33 / 97`
- current role:
  next best follow-on candidate after conjunctivitis

### `anterior_pterygium_vs_normal_v1`

- positive:
  `pterygium`
- negative:
  `normal`
- counts:
  train `72 / 455`
  val `15 / 97`
  test `15 / 97`
- current role:
  longer-shot narrow surface specialist
- caution:
  very small positive class in the current local source

### `anterior_eyelid_abnormality_vs_normal_v1`

- positive:
  `eyelid`
- negative:
  `normal`
- counts:
  train `367 / 455`
  val `79 / 97`
  test `79 / 97`
- current role:
  optional separate branch if eyelid disease remains in product scope

### `anterior_cataract_vs_normal_v1`

- positive:
  `cataract`
- negative:
  `normal`
- current role:
  cataract specialist after `normal_surface`

### `anterior_surface_binary_v1`

- positive:
  `conjunctivitis`, `pterygium`, `uveitis`
- negative:
  `normal`
- excluded:
  `cataract`, `eyelid`
- current role:
  first surface-abnormal router

### `Mendeley Dataset\Original Dataset.zip`

Use for:

- fundus branch only
- DR-vs-healthy
- glaucoma-related fundus experiments

Do not mix its fundus labels into the current anterior app flow.
