Integrate the Batch 008B ChatGPT remaining-candidate review findings as review-support only.

Files expected:
- batch_008B_chatgpt_remaining_manual_review_findings.csv
- batch_008B_accept_dr_pattern_candidates_only.csv
- batch_008B_chatgpt_remaining_manual_review_summary.md
- contact_sheets/

Rules:
- no training
- no fitting
- no app/backend/runtime/model changes
- no preserved package changes
- do not modify reviewed_manifest_v1.csv
- do not modify fitting_manifest_v1.csv
- do not modify challenge_manifest_v1.csv
- do not promote these findings automatically

Suggested destination:
Google Colab/Fundus DR Hem Exudate Separation/review_batches/batch_008B_remaining_dr_pattern_candidate_manual_review/chatgpt_manual_review_findings/

Create an INTEGRATION_NOTE.md stating these are conservative review-support findings only. Verify row counts and manual bucket counts before committing.

Suggested commit message:
docs: add Batch 008B ChatGPT manual review findings
