# reviewed_manifest_v1 Dry-Run Summary

This dry run maps only the 98 Batch 008 proposed accepted DR-pattern rows into
the proposed reviewed-manifest schema.

No canonical `reviewed_manifest_v1.csv` was created.

## Counts

- dry-run row count = 98
- Batch 008A rows = 14
- Batch 008B rows = 84

Bucket count:

- `dr_pattern_dominant = 98`

Status count:

- `accepted = 98`

## Source Class Mix

| Source class | Rows |
| --- | ---: |
| `Moderate` | 87 |
| `Proliferate_DR` | 5 |
| `Severe` | 6 |

## Confidence Mix

| Confidence | Rows |
| --- | ---: |
| `low_medium` | 87 |
| `medium` | 11 |


## Duplicate Checks

- unique `evidence_id` values = 98
- unique `source_row_id` values = 98
- duplicate `evidence_id` count = 0
- duplicate `source_row_id` count = 0

## Safety Statement

This is a dry-run CSV only. It is intentionally named
`reviewed_manifest_v1_dry_run_batch_008_only.csv` and must not be treated as the
canonical `reviewed_manifest_v1.csv`.

No canonical manifest was created yet.
No fitting manifest was created or modified.
No challenge manifest was created or modified.
No training, fitting, model, app, backend, runtime, or preserved-package changes
were made.
