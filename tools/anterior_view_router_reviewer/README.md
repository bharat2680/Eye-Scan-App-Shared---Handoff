# Anterior View Router Reviewer

Simple local browser-based reviewer for the anterior view-router batch CSVs.

## Run

```bash
cd /Users/bharatsharma/Documents/Playground/EyeScan_Shared/tools/anterior_view_router_reviewer
python3 server.py
```

Open:

- `http://127.0.0.1:8010`

## What it edits

The reviewer writes decisions directly back into the selected batch CSV in:

- `/Users/bharatsharma/Documents/Playground/EyeScan_Shared/datasets/anterior/view_router/review_batches`

It only updates:

- `final_router_label`
- `final_include_in_router`
- `review_status`
- `review_notes`

Seed columns stay unchanged.

## Resume behavior

- every change autosaves back into the batch CSV
- the browser remembers the last viewed row per batch in local storage
- `Jump to first pending` returns to the next unreviewed row quickly

## Initial batch

The app starts with:

- `labels_review_batch_01_eyelid_dominant_first.csv`

But the batch dropdown makes it easy to switch to batch 02 or batch 03 later.
