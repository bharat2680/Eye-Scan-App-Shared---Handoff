# Fundus DR Hem Exudate Separation V1 Dataset Source Inventory

## Purpose And Safety Warning

This document inventories possible existing dataset sources for the future
`fundus_dr_hem_exudate_separation_v1` planning lane.

This is documentation only. It does not approve training, does not create model
artifacts, does not copy or move datasets, and does not promote this lane as
production.

Do not modify Flutter code, backend inference code, model loading logic,
deployment files, runtime arbitration, or package artifacts from this lane.

## Preserved Baseline Warning

Preserved baselines remain unchanged:

- `anterior_boundary_v1_efficientnetb0_colab_package.zip`
- `fundus_broad_abnormality_v1_efficientnetb0_colab_package.zip`

Comparison-only evidence remains comparison-only:

- `anterior_boundary_v1_efficientnetb0_colab_package (1).zip`
- `fundus_broad_abnormality_v1_efficientnetb2_colab_package.zip`

This inventory must not be used to replace
`fundus_broad_abnormality_v1_efficientnetb0_colab_package.zip`.

## Core Label Set

The future manifest must support exactly these five labels:

- `normal_or_non_specific`
- `dr_pattern_dominant`
- `hemorrhage_pattern_dominant_non_dr`
- `exudate_macular_pattern_dominant`
- `mixed_hemorrhage_exudate_pattern`

Source labels are not final labels. Source labels can suggest candidates, but
training can only use `final_label` from reviewed manifest rows.

Labels must be string-mapped, not numeric-index-mapped.

## Candidate Dataset And Source Inventory

Counts below are rough local file counts observed from visible folders only.
If a source was not visible locally, this document uses "not found locally" or
"requires Drive/Colab confirmation" instead of inventing counts.

| Source | Local or repo path visible now | Rough visible counts | Likely usable classes | Possible five-label mapping | Review requirement | Risk | Notes |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| Existing broad-abnormality curation CSV | `/Users/bharatsharma/Documents/EyeScan_Local_Data/datasets/fundus/broad_abnormality_v1/reviewed_manifest.csv` | `65` review rows: `48` accepted, `6` needs second review, `10` challenge only, `1` exclude | Prior reviewed seeds and boundary examples | `healthy_fundus` may map to `normal_or_non_specific`; `diabetic_retinopathy_like` may map to `dr_pattern_dominant`; old `hemorrhage_exudate_like` rows need re-review into hemorrhage, exudate, or mixed | Full image-level relabel into the new five-class taxonomy required | Medium | Best starting point because review notes already exist, but prior labels are too broad for this lane. |
| Existing broad-abnormality curation archive | `/Users/bharatsharma/Documents/EyeScan_Local_Data/datasets/fundus/broad_abnormality_v1.zip` | Archive contains curation CSVs and helper docs, not an image corpus | Review metadata only | Same as curation CSV if restored or compared | Review metadata only; do not treat archive entries as final labels | Medium | Useful for history/backups, not a direct image source. |
| Repo narrowed broad-abnormality manifest | `datasets/manifests/fundus_broad_abnormality_v1.jsonl` | `46` rows in prior narrowed baseline manifest | Historical source references only | May help locate previous healthy, DR-like, and hemorrhage/exudate-like examples | Must not be used directly as final labels for this lane | Medium | Tied to preserved/comparison baseline work. Use as reference only, not as a new training manifest. |
| Eye-Fundus glaucoma/healthy extracted folder | `/Users/bharatsharma/Documents/EyeScan_Local_Data/datasets/fundus/Eye_Fundus_Glaucoma_vs_Healthy` | Healthy `2676`; Glaucoma `2880` | Clean normal/non-specific controls and hard negative review examples | Healthy candidates may map to `normal_or_non_specific`; glaucoma images are not a target class but may help challenge/hard-negative review | Manual sampling review required before `final_label`; glaucoma rows should usually not enter this lesion-pattern lane | Low for normal controls, medium for hard negatives | Good visible source for normal controls. Not a DR/hemorrhage/exudate separation source. |
| Eye Disease Image Dataset, Original Dataset | `/Volumes/My Passport/EyeScan App/Datasets/Augmented Dataset-Kaggle/Eye Disease Image Dataset/Original Dataset` | Central Serous Chorioretinopathy `101`; Diabetic Retinopathy `1509`; Disc Edema `127`; Glaucoma `1349`; Healthy `1024`; Macular Scar `444`; Myopia `500`; Pterygium `17`; Retinal Detachment `125`; Retinitis Pigmentosa `139` | DR-pattern candidates, healthy controls, macular/exudate-like candidates, mixed lesion candidates | Diabetic Retinopathy may map to `dr_pattern_dominant`, `mixed_hemorrhage_exudate_pattern`, or focal exudate/hemorrhage labels after review; Healthy may map to `normal_or_non_specific`; Macular Scar/CSC/Disc Edema require caution and may not fit this lane | Image-level review required; source disease folder is never final label | Medium | Mounted locally now. Strong candidate for starter manifest sampling, especially DR and healthy rows. Non-DR hemorrhage coverage is not obvious from folder names. |
| My Passport diabetic-retinopathy folder used by prior curation | `/Volumes/My Passport/EyeScan App/Datasets/Augmented Dataset-Kaggle/Eye Disease Image Dataset/Original Dataset/Diabetic Retinopathy` | `1509` images | DR-pattern, mixed hemorrhage/exudate, focal exudate or focal hemorrhage candidates | Review into `dr_pattern_dominant`, `exudate_macular_pattern_dominant`, `mixed_hemorrhage_exudate_pattern`, or rarely hemorrhage-dominant if pattern supports it | Full image-level review required | Medium | Likely easiest lesion-positive source, but broad DR source labels will over-collapse this lane if used without review. |
| Desktop manual fundus captures | `/Users/bharatsharma/Desktop/Eye Images Test/Fundus Images` | `12` visible image files | Small manual hard cases and possible challenge examples | Could support DR-like, hemorrhage/exudate, mixed, or normal/non-specific only after review | Manual review required; best for challenge/starter rows, not scale | Medium | Very small and likely capture-specific. Useful for boundary examples, not enough for training. |
| IDRiD DR-vs-healthy staging path from older docs | `/Users/bharatsharma/Desktop/Eye Scan App Handoff/Datasets 2026/External Fundus/IDRiD_DR_vs_Healthy` | Not found locally | DR-pattern and healthy controls if restored | Likely `dr_pattern_dominant` and `normal_or_non_specific` after review | Requires Drive/local confirmation and image-level review | Medium | Existing Colab docs reference IDRiD runs, but this local staging path is not present now. |
| IDRiD Colab raw archive reference | `MyDrive/Datasets/B. Disease Grading.zip` | Requires Drive/Colab confirmation | DR-pattern and healthy controls | `dr_pattern_dominant` and `normal_or_non_specific`, with possible mixed/exudate examples after review | Requires Drive/Colab confirmation and image-level review | Medium | Useful future source if accessible in Drive. Do not infer counts locally. |
| PAPILA staging path from older docs | `/Users/bharatsharma/Desktop/Eye Scan App Handoff/Datasets 2026/External Fundus/PAPILA_Glaucoma_vs_Healthy` | Not found locally | Mostly glaucoma/healthy, not a direct target for this lane | Healthy rows may map to `normal_or_non_specific`; glaucoma rows are usually out of scope except hard-negative/challenge review | Requires local confirmation and manual review | Medium | Not a primary DR/hemorrhage/exudate source. |
| RFMiD or other multi-disease retinal sources from older docs | Not found locally in inspected Mac paths | Requires Drive/Colab or external-disk confirmation | Potential non-DR vascular, exudate, mixed, and structural retinal examples if labels are available | Possible source for `hemorrhage_pattern_dominant_non_dr`, `exudate_macular_pattern_dominant`, and mixed examples after review | Requires source availability confirmation, label-file confirmation, and image-level review | High | Potentially valuable, but not available as a confirmed local source in this pass. |

## Class Coverage Table

| Planned label | Possible sources | Sourcing risk | Manual review required | Notes |
| --- | --- | --- | --- | --- |
| `normal_or_non_specific` | Eye-Fundus Healthy, Eye Disease Image Dataset Healthy, existing broad-abnormality healthy rows, IDRiD healthy if restored | Low | Yes | Likely easiest class to source. Still requires quality and pathology-threshold review. |
| `dr_pattern_dominant` | Eye Disease Image Dataset Diabetic Retinopathy, IDRiD if restored, existing broad-abnormality DR-like rows | Medium | Yes | Likely easier lesion-positive class, but broad DR folder labels must not become final labels without image-level review. |
| `hemorrhage_pattern_dominant_non_dr` | Existing manual fundus examples if suitable, old hemorrhage/exudate rows after re-review, future RFMiD or vascular retinal source if confirmed | High | Yes | Highest-risk class. No clean local non-DR hemorrhage-specific folder was confirmed in this pass. |
| `exudate_macular_pattern_dominant` | Eye Disease DR focal cases, Macular Scar/CSC/Disc Edema folders only if image pattern fits, old hemorrhage/exudate rows after re-review | Medium to high | Yes | Needs careful review because source disease names may not correspond to exudate/macular pattern. |
| `mixed_hemorrhage_exudate_pattern` | Eye Disease DR mixed cases, old hemorrhage/exudate rows after re-review, manual fundus hard cases | Medium to high | Yes | Needs careful review. Must not be used as a vague catch-all for uncertain or low-quality rows. |

## Key Sourcing Conclusions

Highest-risk class:

- `hemorrhage_pattern_dominant_non_dr`

Reason: no clean local folder specifically representing non-DR
hemorrhage-dominant vascular patterns was confirmed. This class may need a
dedicated source, careful manual capture review, or a future multi-disease
retinal dataset with usable vascular labels.

Likely easier classes:

- `normal_or_non_specific`
- `dr_pattern_dominant`

Reason: visible local sources include healthy controls and a large diabetic
retinopathy folder, though both still require image-level review and
`final_label` assignment.

Classes needing careful review:

- `exudate_macular_pattern_dominant`
- `mixed_hemorrhage_exudate_pattern`

Reason: exudates and hemorrhages often co-occur, especially in diabetic
retinopathy. Source folders may provide candidates, but the five-class label
depends on visible pattern dominance, not the source folder name.

## Source-Label Rules

- Source labels are not final labels.
- `proposed_label` may come from source mapping, folder names, or old manifests.
- Future training can only use `final_label` from reviewed manifest rows.
- `final_label` should stay empty until an image has been reviewed under this
  five-class taxonomy.
- Low-quality or uncertain rows should not be forced into a class.
- `mixed_hemorrhage_exudate_pattern` must not be used as a vague catch-all.
- `challenge_only` rows must remain outside train/val/test fitting.

## Recommended Next Step

Do not train next.

The next safe step after this inventory is to build a small starter manifest
sample using `manifest_templates/manifest_template.csv`.

Recommended starter sample shape:

- a small reviewed batch for `normal_or_non_specific`
- a small reviewed batch for `dr_pattern_dominant`
- a small exploratory batch for `exudate_macular_pattern_dominant`
- a small exploratory batch for `mixed_hemorrhage_exudate_pattern`
- a very cautious search batch for `hemorrhage_pattern_dominant_non_dr`
- a separate held-out challenge-only batch for known boundary cases

That starter manifest should remain review/planning data only until class
coverage, duplicate handling, image quality, and source leakage are checked.
