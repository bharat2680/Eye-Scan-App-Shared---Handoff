Integrate the Batch 008A ChatGPT manual review findings as review-support only.

Uploaded handoff contents expected:
- batch_008A_chatgpt_manual_review_findings.csv
- batch_008A_accept_dr_pattern_candidates_only.csv
- batch_008A_chatgpt_manual_review_summary.md

Strict rules:
- no training
- no fitting
- no model/app/backend/runtime changes
- no preserved package changes
- do not modify reviewed_manifest_v1.csv
- do not modify fitting_manifest_v1.csv
- do not modify challenge_manifest_v1.csv
- do not promote rows automatically

Task:
1. Copy these files into the Batch 008A folder under `chatgpt_manual_review_findings/`.
2. Create an INTEGRATION_NOTE.md explaining that these are conservative visual review findings and not a manifest update.
3. Verify row count = 160.
4. Verify manual bucket counts exactly match the summary.
5. Verify accepted clean DR candidates count from `accept_dr_pattern_dominant`.
6. Show git diff summary.
7. Commit only review-support files if diff is clean.

Suggested commit message:
docs: add Batch 008A ChatGPT manual review findings
