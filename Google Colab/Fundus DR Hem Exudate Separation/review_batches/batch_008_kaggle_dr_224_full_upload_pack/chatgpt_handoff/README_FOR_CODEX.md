# Batch 008 Codex handoff

Included files:
- `batch_008_full_index_enriched.csv`
- `batch_008_priority_review_order.csv`
- `batch_008_review_note.md`

Purpose:
These files are for the EyeScan fundus DR evidence lane and should be used as review support only.

Important constraints:
- review-only first
- no training
- no app/backend/runtime changes
- no manifest promotion unless explicitly instructed later
- no preserved package changes

How to use:
1. Treat `batch_008_full_index_enriched.csv` as the working review scaffold.
2. Treat `auto_*` columns as automated quality-triage helpers only, not diagnostic truth.
3. Use `batch_008_priority_review_order.csv` to review in this suggested order:
   - Severe first
   - Proliferate_DR second
   - Moderate third
4. Keep all lesion-level review conclusions manual / visually confirmed.

Current status:
- Cross-check completed on uploaded pack.
- Counts verified:
  - Moderate: 999
  - Severe: 193
  - Proliferate_DR: 295
  - Total: 1487
- Manual lesion-level adjudication for all rows has NOT yet been completed.
