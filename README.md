# EyeScan Shared

This folder is the shared coordination layer for the Mac Codex app and the Dell Codex app.

## What belongs here

- handoff docs
- status docs
- training priorities
- dataset mapping
- small metadata files
- model package notes and contracts

## What should not live here by default

- raw datasets
- large exported PDFs
- large `.keras` artifacts unless Git LFS is intentionally used

## Current shared workflow

1. Mac or Dell updates files in `EyeScan_Shared/`
2. commit the changes
3. push to GitHub
4. the other machine pulls the latest changes
5. local Codex on that machine reads the updated local repo copy

## Main docs

- `docs/README.md`
- `docs/APP_INTEGRATION_STATUS.md`
- `docs/CODEX_HANDOFF.md`
- `docs/DATASET_MAPPING.md`
- `docs/EXPORT_REVIEW_NOTES.md`
- `docs/FOUNDATION_MODEL_DOWNLOADS.md`
- `docs/MODEL_STATUS.md`
- `docs/PLAY_MONETIZATION_PLAN.md`
- `docs/TRAINING_PRIORITIES.md`
- `SYNC_INSTRUCTIONS.md`
