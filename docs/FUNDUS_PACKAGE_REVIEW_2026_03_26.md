# Fundus Package Review - 2026-03-26

This review is the Mac-side verification checkpoint for the newest local fundus
packages. It is intentionally separate from the in-progress training-thread
handoff edits so we do not disturb active model notes while Colab jobs are
paused.

## Reviewed packages

| Package | Current verdict | Why | Next action |
| --- | --- | --- | --- |
| `fundus_dr_idrid_v3_efficientnetb2_balanced_colab_package.zip` | `promote_backend_hidden` | Best current DR specialist. Test accuracy `0.7961`, balanced accuracy `0.8105`. Clear improvement over both local `v1` and Colab `v2`. | Keep in backend fundus branch. Do not expose in app UI until fundus release is intentionally enabled. |
| `fundus_glaucoma_eyefundus_v3_efficientnetb0_colab_package.zip` | `backend_only_fallback` | Strongest completed glaucoma fallback so far, but still a fallback rather than a final glaucoma release model. Test accuracy `0.7720`, balanced accuracy `0.7730` at tuned threshold. | Keep as hidden fallback behind the fundus branch while stronger glaucoma specialists continue. |
| `fundus_dr_idrid_v2_efficientnetb0_colab_package.zip` | `archive_superseded` | Valid export, but it is weaker than `IDRiD v3` and no longer the preferred candidate. Test accuracy `0.7670`, balanced accuracy `0.7440`. | Keep only for comparison/history. Do not integrate further. |

## Training lanes not yet reviewable

| Training lane | Current verdict | Why | Next action |
| --- | --- | --- | --- |
| `fundus_glaucoma_chaksu_v1_efficientnetb2_colab` / `v2` lane | `training_paused_no_package` | Notebook and training scripts exist locally, but no final packaged artifact is available for verification yet. Current Colab state is paused because GPU access ran out. | Resume later in Colab when GPU is available again, then produce a backend-style package zip for review. |

## Practical interpretation

- The app should remain **anterior-first** for now.
- The backend can safely keep the hidden fundus branch with:
  - `fundus_dr_idrid_v3_efficientnetb2_balanced_colab`
  - `fundus_glaucoma_eyefundus_v3_efficientnetb0_colab`
- The next fundus package worth serious promotion review is the first completed
  `Chaksu` glaucoma package.

## Release guidance

- **Do not expose fundus in the public app flow yet.**
- **Do not judge fundus quality from anterior app testing.**
- **Do keep the hidden backend fundus path available for controlled testing and
  future integration.**

## Short promotion table

- `fundus_dr_idrid_v3_efficientnetb2_balanced_colab`: promote for hidden
  backend fundus DR branch
- `fundus_glaucoma_eyefundus_v3_efficientnetb0_colab`: keep as hidden glaucoma
  fallback
- `fundus_dr_idrid_v2_efficientnetb0_colab`: archive/superseded
- `fundus_glaucoma_chaksu_*`: training paused, await package
