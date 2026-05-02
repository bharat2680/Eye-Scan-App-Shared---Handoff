# Prompt for Codex: Batch 008 ChatGPT candidate findings integration

Use the attached ChatGPT candidate findings handoff.

Files:
- batch_008_chatgpt_candidate_findings.csv
- batch_008_candidate_shortlist_for_manual_review.csv
- batch_008_chatgpt_candidate_findings_summary.md
- candidate_contact_sheets/

Important interpretation:
- These are AI-assisted visual triage findings only.
- They are NOT final medical labels.
- They are NOT accepted evidence labels.
- They must NOT be used directly for training.
- `chatgpt_candidate_review_bucket` is a candidate bucket only.
- `usable_for_training_candidate` means candidate for later manual acceptance, not approved for fitting.

Strict rules:
- no training
- no fitting
- no app/backend/runtime changes
- no model changes
- no preserved package changes
- do not modify reviewed_manifest_v1.csv unless Bharat explicitly approves a later manual-accepted batch
- do not modify fitting_manifest_v1.csv
- do not modify challenge_manifest_v1.csv

Task:
1. Copy this handoff into the Batch 008 review folder under:
   chatgpt_candidate_findings/

2. Verify:
   - total rows = 1487
   - Moderate = 999
   - Severe = 193
   - Proliferate_DR = 295

3. Summarise candidate bucket counts from `chatgpt_candidate_review_bucket`.

4. Create a small manual adjudication plan from:
   batch_008_candidate_shortlist_for_manual_review.csv

Suggested future manual review batches:
- Batch 008A: top dr_pattern_dominant candidates
- Batch 008B: top mixed_hemorrhage_exudate_pattern candidates
- Batch 008C: exudate/macular candidates only if needed
- Batch 008D: needs_second_review / low-quality audit

Do not create accepted evidence rows yet.
Do not promote candidate labels.
Do not train.

Return:
- files copied
- row count verification
- bucket count summary
- proposed manual review batch sizes
- git diff summary
- confirm no forbidden files changed
