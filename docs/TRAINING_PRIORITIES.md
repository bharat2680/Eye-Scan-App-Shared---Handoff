# Training Priorities

Last updated: 2026-03-17 00:07 Australia/Sydney

## Product truth

- the app already has an honest evaluation-only anterior screening pipeline
- the biggest remaining weakness is the vague `surface_abnormal` bucket
- glaucoma can wait for now unless it is already mid-run

## Highest-priority next training work

Do next:

1. train `uveitis_vs_normal`
2. train `pterygium_vs_normal`
3. train `eyelid_abnormality_vs_normal` only if eyelid disease is still in scope
4. keep glaucoma separate from the current anterior app branch

## Exact training sequence

1. regenerate manifests:

```powershell
python scripts/prepare_manifests.py
```

2. train conjunctivitis specialist:

```powershell
python training/anterior/train.py --config configs/anterior_conjunctivitis_vs_normal_v1_simplecnn.json
```

3. train uveitis specialist:

```powershell
python training/anterior/train.py --config configs/anterior_uveitis_vs_normal_v1_simplecnn.json
```

4. train pterygium specialist:

```powershell
python training/anterior/train.py --config configs/anterior_pterygium_vs_normal_v1_simplecnn.json
```

5. train eyelid specialist if still in scope:

```powershell
python training/anterior/train.py --config configs/anterior_eyelid_abnormality_vs_normal_v1_simplecnn.json
```

## Current best package already available

- `anterior_conjunctivitis_vs_normal_v1_simplecnn`
- local package path on Dell:
  `C:\Users\HP\OneDrive\Documents\Playground\handoff\macbook_next_specialist_packages\anterior_conjunctivitis_vs_normal_v1_simplecnn_package`
- decision threshold:
  `0.15` on `p(conjunctivitis)`
- deployment recommendation:
  integrated on Mac as `evaluation_only`

## Keep separate for now

- glaucoma work
- general fundus multi-class work

Reason:

- those belong to the fundus branch, not the current anterior app flow
