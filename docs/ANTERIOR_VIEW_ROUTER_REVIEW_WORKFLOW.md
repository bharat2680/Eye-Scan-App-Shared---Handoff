# Anterior View Router Review Workflow

This pass is for **human review support only**. Do not start training from the
seeded sheet directly.

## Goal

Correct the heuristic labels in
[labels_seeded_first_pass.csv](/Users/bharatsharma/Documents/Playground/EyeScan_Shared/datasets/anterior/view_router/labels_seeded_first_pass.csv)
into reviewed final labels while keeping the process low-risk and easy to audit.

Target label space remains strict:

- `iris_visible`
- `eyelid_dominant`
- `unclear`

## Reviewer Workflow

Use the seeded CSV as the primary review sheet. The key columns are:

- `router_label`
  - seed label only; leave untouched for auditability
- `include_in_router`
  - seed include flag only; leave untouched for auditability
- `final_router_label`
  - fill this only when the final reviewed label differs from the seed label
- `final_include_in_router`
  - fill this only when the final reviewed include decision differs from the seed include flag
- `review_status`
  - recommended values:
    - `confirmed_seed`
    - `changed_seed`
    - `excluded_from_router`
    - `needs_second_pass`
- `review_notes`
  - short reason for the change or ambiguity

### Review rule

If the seed looks correct:

- leave `final_router_label` blank
- leave `final_include_in_router` blank
- set `review_status=confirmed_seed`

If the seed needs correction:

- set `final_router_label` to the final label
- set `final_include_in_router` to `1` or `0` if the include decision also changes
- set `review_status=changed_seed`
- add a short `review_notes` reason

If the image should stay out of router training:

- optionally set `final_router_label` if the class is known
- set `final_include_in_router=0`
- set `review_status=excluded_from_router`

If the image is still ambiguous:

- leave a review note
- set `review_status=needs_second_pass`

## Recommended Review Batching

The seeded CSV now includes `suggested_review_batch`.

Recommended pass order:

1. `eyelid_dominant_first`
   - review every seeded eyelid-dominant row first
   - goal: rescue iris-visible eyelid-folder images before they bias the router
2. `unclear_second`
   - review all unclear rows next
   - split them into:
     - true `unclear`
     - rescued `eyelid_dominant`
     - rescued `iris_visible`
3. `iris_visible_high_risk_next`
   - review high-risk iris-visible rows next
   - especially rows flagged with:
     - `very_low_resolution`
     - `extreme_aspect`
     - `manual_review_for_router_bias`
     - `square_normal_source`
4. `iris_visible_spotcheck_last`
   - final spot-check pass for the lower-risk iris-visible rows

### Pre-filtered reviewer CSVs

To avoid editing the full master sheet during the first reviewer passes, generate
pre-filtered CSVs that preserve all review columns plus duplicate-group context:

```bash
python3 /Users/bharatsharma/Documents/Playground/EyeScan_Shared/scripts/export_view_router_review_batches.py
```

Default outputs:

- `review_batches/labels_review_batch_01_eyelid_dominant_first.csv`
- `review_batches/labels_review_batch_02_unclear_second.csv`
- `review_batches/labels_review_batch_03_iris_visible_high_risk_next.csv`

Each batch CSV includes:

- all master review columns from `labels_seeded_first_pass.csv`
- duplicate / near-duplicate group metadata
- peer-path hints so grouped images can be reviewed together

Important:

- treat batch CSVs as reviewer workbooks only
- after review, copy the final decisions back into the master seeded sheet
- then export `labels_reviewed_final.csv` from the master sheet

## Duplicate / Near-Duplicate Review Support

Use the review-groups artifact to review clusters together instead of row by row:

- [labels_seeded_review_groups.csv](/Users/bharatsharma/Documents/Playground/EyeScan_Shared/datasets/anterior/view_router/labels_seeded_review_groups.csv)
- [labels_seeded_review_groups_summary.json](/Users/bharatsharma/Documents/Playground/EyeScan_Shared/datasets/anterior/view_router/labels_seeded_review_groups_summary.json)

Group types:

- `exact_duplicate`
  - same file content; review once and apply the same final decision to the whole group
- `near_duplicate_candidate`
  - visually similar images from the same source folder; review together to keep routing labels consistent

## Exact Command Sequence

### 1. Regenerate the seeded review sheet if needed

```bash
python3 /Users/bharatsharma/Documents/Playground/EyeScan_Shared/scripts/seed_view_router_labels.py
```

### 2. Regenerate duplicate / near-duplicate review groups

```bash
python3 /Users/bharatsharma/Documents/Playground/EyeScan_Shared/scripts/find_view_router_review_groups.py
```

### 3. Human review the seeded CSV

Review and edit:

- [labels_seeded_first_pass.csv](/Users/bharatsharma/Documents/Playground/EyeScan_Shared/datasets/anterior/view_router/labels_seeded_first_pass.csv)

Optional first-pass reviewer workbooks:

- [labels_review_batch_01_eyelid_dominant_first.csv](/Users/bharatsharma/Documents/Playground/EyeScan_Shared/datasets/anterior/view_router/review_batches/labels_review_batch_01_eyelid_dominant_first.csv)
- [labels_review_batch_02_unclear_second.csv](/Users/bharatsharma/Documents/Playground/EyeScan_Shared/datasets/anterior/view_router/review_batches/labels_review_batch_02_unclear_second.csv)
- [labels_review_batch_03_iris_visible_high_risk_next.csv](/Users/bharatsharma/Documents/Playground/EyeScan_Shared/datasets/anterior/view_router/review_batches/labels_review_batch_03_iris_visible_high_risk_next.csv)

### 4. Export reviewed labels into a manifest-ready final CSV

```bash
python3 /Users/bharatsharma/Documents/Playground/EyeScan_Shared/scripts/export_reviewed_view_router_labels.py \
  --input-csv /Users/bharatsharma/Documents/Playground/EyeScan_Shared/datasets/anterior/view_router/labels_seeded_first_pass.csv \
  --output-csv /Users/bharatsharma/Documents/Playground/EyeScan_Shared/datasets/anterior/view_router/labels_reviewed_final.csv
```

### 5. Validate reviewed labels before manifest rebuild

```bash
python3 /Users/bharatsharma/Documents/Playground/EyeScan_Shared/scripts/validate_view_router_labels.py \
  --input-csv /Users/bharatsharma/Documents/Playground/EyeScan_Shared/datasets/anterior/view_router/labels_reviewed_final.csv \
  --require-no-pending
```

Optional stricter floor check:

```bash
python3 /Users/bharatsharma/Documents/Playground/EyeScan_Shared/scripts/validate_view_router_labels.py \
  --input-csv /Users/bharatsharma/Documents/Playground/EyeScan_Shared/datasets/anterior/view_router/labels_reviewed_final.csv \
  --require-no-pending \
  --min-included-per-label 50
```

### 6. Rebuild the manifest from the reviewed final CSV

```bash
python3 /Users/bharatsharma/Documents/Playground/EyeScan_Shared/scripts/build_view_router_manifest.py \
  --spec /Users/bharatsharma/Documents/Playground/EyeScan_Shared/configs/anterior_view_router_v1_dataset_spec.json \
  --label-csv /Users/bharatsharma/Documents/Playground/EyeScan_Shared/datasets/anterior/view_router/labels_reviewed_final.csv
```

## Low-Risk Review Rules

- never overwrite the seed columns
- always preserve reviewer reasoning in `review_notes` when changing a label
- prefer `needs_second_pass` over forcing a weak label
- review duplicate / near-duplicate groups together to avoid inconsistent labels
- do not start training until label validation passes cleanly
