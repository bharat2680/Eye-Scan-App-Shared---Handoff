# Batch 008 ChatGPT candidate findings summary

Scope: AI-assisted visual triage across all 1487 images in the uploaded Batch 008 Kaggle DR 224 review pack.

Important boundary: these are **candidate review findings**, not medical diagnoses, not ophthalmologist labels, and not direct training labels. Use them to create smaller manual-review candidate batches only.

## Source class counts
- Moderate: 999
- Severe: 193
- Proliferate_DR: 295
- Total: 1487

## Candidate bucket counts
- mixed_hemorrhage_exudate_pattern: 1147
- dr_pattern_dominant: 335
- needs_second_review: 4
- exudate_macular_pattern_dominant: 1

## Source class by candidate bucket

### Moderate
- mixed_hemorrhage_exudate_pattern: 765
- dr_pattern_dominant: 230
- needs_second_review: 3
- exudate_macular_pattern_dominant: 1

### Severe
- mixed_hemorrhage_exudate_pattern: 159
- dr_pattern_dominant: 34

### Proliferate_DR
- mixed_hemorrhage_exudate_pattern: 223
- dr_pattern_dominant: 71
- needs_second_review: 1

## Recommended next lane
1. Do not train yet.
2. Ask Codex to import `batch_008_chatgpt_candidate_findings.csv` as review-support only.
3. Create smaller manual adjudication batches from `batch_008_candidate_shortlist_for_manual_review.csv`, prioritising `dr_pattern_dominant` and `mixed_hemorrhage_exudate_pattern` candidates with quality score >= 55.
4. Only after manual acceptance should rows be considered for reviewed evidence; do not touch fitting/challenge manifests in this lane.

## Caveat
This pass uses visual/image-feature proxies and source-class context. It is useful for triage but does not replace human/clinical adjudication.
