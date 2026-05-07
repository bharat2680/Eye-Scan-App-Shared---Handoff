# Data Access Notes

## Manifest Source

The baseline scaffold uses:

- `Google Colab/Fundus DR Hem Exudate Separation/review_manifests/fitting_manifest_v1.csv`

That manifest points to externally stored image paths or archive-member style
paths collected during the reviewed-evidence lane.

## Raw Image Storage

- Raw images are not committed to the repository.
- The training runtime must resolve image paths safely outside the repo.
- Any large dataset extraction or staging must stay outside the repo.

## Repo Safety

- Do not copy full raw image sets into the repository.
- Do not create app/backend dependencies on external training paths.
- Do not assume every runtime environment has the same external mount points.

## Training Runtime Responsibility

A future training runtime should:

- read `fitting_manifest_v1.csv`
- verify required columns and split counts
- resolve image paths carefully
- fail loudly on missing files instead of silently skipping data

## Non-Goals

This scaffold does not:

- extract raw datasets into the repo
- create backend dependencies
- change reviewed or fitting manifests
- approve production data plumbing
