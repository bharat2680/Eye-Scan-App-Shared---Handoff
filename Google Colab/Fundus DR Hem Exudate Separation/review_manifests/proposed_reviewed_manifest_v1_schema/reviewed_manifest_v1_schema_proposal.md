# reviewed_manifest_v1.csv Schema Proposal

## Scope

This document proposes a canonical schema for `reviewed_manifest_v1.csv` in the
EyeScan fundus DR evidence lane.

This is schema proposal only. It does not create the final
`reviewed_manifest_v1.csv`, does not approve fitting, and does not approve
training.

## Why reviewed_manifest_v1.csv Does Not Currently Exist

The current lane has raw candidate manifests, review batches, ChatGPT visual
review handoffs, and proposed evidence-addition files, but no canonical reviewed
manifest has been created under:

`Google Colab/Fundus DR Hem Exudate Separation/`

Codex correctly blocked direct promotion because there was no existing reviewed
manifest schema to inspect or append to. This proposal defines the schema before
any canonical manifest is created.

## Purpose Of reviewed_manifest_v1.csv

`reviewed_manifest_v1.csv` should be the source-of-truth table for reviewed
fundus DR evidence rows after manual or explicitly approved visual review.

It should capture:

- a stable evidence identifier
- traceability back to source dataset and review batch
- the reviewed evidence bucket
- review status
- reviewer and review method
- review notes and quality notes
- enough image path information for later validation/export gates

It is still not a fitting manifest. Fitting and challenge manifests must be
created later through explicit approval and separate validation.

## Proposed Canonical Columns

| Column | Purpose |
| --- | --- |
| `evidence_id` | Stable unique reviewed-evidence identifier. |
| `source_lane` | Lane or task namespace, for example `fundus_dr_evidence`. |
| `source_batch` | Source acquisition or review batch family. |
| `source_review_batch` | Specific review pass that produced the decision. |
| `source_dataset` | Human-readable dataset/source name. |
| `source_class` | Original source class/folder/label when available; not final truth. |
| `source_row_id` | Original row identifier from the review pack. |
| `id_code` | Dataset image identifier when available. |
| `image_path` | Traceable image path relative to this repo/workspace source pack. |
| `review_bucket` | Final reviewed evidence bucket. |
| `review_status` | Review decision state such as `accepted` or `needs_second_review`. |
| `reviewer` | Reviewer or review system. |
| `review_method` | Review method, for example `conservative_contact_sheet_review`. |
| `confidence` | Reviewer confidence or inherited review confidence if available. |
| `quality_score` | Review-support quality score if available. |
| `lesion_pattern_notes` | Notes about lesion/pattern evidence. |
| `quality_notes` | Image quality notes. |
| `source_findings_file` | CSV or handoff file from which the row was promoted. |
| `accepted_at_stage` | Stage that accepted or proposed the row. |
| `notes` | Additional safety and traceability notes. |

## Review Status Representation

Accepted rows:

- `review_status = accepted`
- `review_bucket` contains the reviewed evidence bucket
- `accepted_at_stage` records the review/promotion stage
- source labels remain traceability only and must not be treated as final truth

Rejected or downgraded rows:

- should not be silently dropped if they are included in a reviewed manifest
- can use `review_status = rejected` or a lane-approved equivalent if a future
  schema revision decides to retain rejected rows
- `review_bucket` should contain the reviewer-assigned downgrade bucket when
  useful, or remain blank if the row is excluded from evidence accounting

Needs-second-review rows:

- `review_status = needs_second_review`
- `review_bucket` should contain the tentative bucket only if explicitly useful
  for routing
- these rows must not enter fitting or evidence-count totals as accepted rows

Challenge-only rows:

- should use a separate challenge lane or a `review_status = challenge_only`
  convention only after explicit approval
- they must not enter fitting unless a future challenge workflow explicitly
  requires it

## Source Traceability

Every row should preserve source traceability through:

- `source_batch`
- `source_review_batch`
- `source_dataset`
- `source_class`
- `source_row_id`
- `id_code`
- `image_path`
- `source_findings_file`

For Batch 008, `image_path` should trace back to the upload pack under:

`Google Colab/Fundus DR Hem Exudate Separation/review_batches/batch_008_kaggle_dr_224_full_upload_pack/images/`

## Historical Batch 001-007 Handling

Batch 001-007 reviewed evidence should be backfilled later in a separate pass.
That pass should:

1. inventory each historical ChatGPT visual review CSV
2. map its existing columns into this proposed schema
3. preserve each row's original source image path and review batch
4. retain accepted, needs-second-review, and downgraded states only according to
   a documented policy
5. verify the expected pre-Batch-008 accepted `dr_pattern_dominant` count of 37
6. avoid creating fitting or challenge manifests

Historical rows should not be mixed into the Batch 008 dry-run file created in
this folder.

## Batch 008 Proposed Accepted Row Mapping

Batch 008 proposed additions map as follows:

| Proposed-addition field | Dry-run reviewed-manifest field |
| --- | --- |
| `proposed_addition_id` | source reference only; dry-run creates new `evidence_id` |
| `source_batch` | source-review provenance; dry-run normalizes `source_batch` to `batch_008_kaggle_dr_224` |
| `row_id` | `source_row_id` |
| `source_dataset` | normalized to `Kaggle Diabetic Retinopathy 224x224 2019` |
| `source_class` | `source_class` |
| `id_code` | `id_code` |
| `relative_image_path` | `image_path`, prefixed with the Batch 008 upload-pack folder |
| `accepted_bucket` | `review_bucket` |
| `reviewer_decision` | represented by `review_status = accepted` and notes |
| `confidence` | `confidence` |
| `quality_score` | `quality_score` |
| `lesion_pattern_notes` | `lesion_pattern_notes` |
| `quality_notes` | `quality_notes` |
| `source_findings_file` | `source_findings_file` |

For the dry-run rows:

- `review_bucket = dr_pattern_dominant`
- `review_status = accepted`
- `reviewer = ChatGPT_visual_review`
- `review_method = conservative_contact_sheet_review`
- `accepted_at_stage = proposed_reviewed_manifest_v1_dry_run`

## Safety Boundary

This is schema proposal only.

No final `reviewed_manifest_v1.csv` was created.
No `fitting_manifest_v1.csv` was created or modified.
No `challenge_manifest_v1.csv` was created or modified.
No training, fitting, model, app, backend, runtime, or preserved-package changes
are approved by this proposal.
