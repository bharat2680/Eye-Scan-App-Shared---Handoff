# GitHub Sync Instructions

Use these steps on both the Mac and the Dell.

## One-time setup

1. Create an empty GitHub repo, for example:
   - `EyeScan_Shared`
2. On the Mac, from `/Users/bharatsharma/Documents/Playground`:

```bash
git remote add origin <your-github-repo-url>
git add EyeScan_Shared
git commit -m "Add EyeScan shared handoff docs"
git push -u origin main
```

3. On the Dell, clone the same repo locally.

Example Windows path:

```powershell
cd C:\Users\HP\Documents
git clone <your-github-repo-url> Playground
```

If `Playground` already exists on Dell, clone into another folder such as:

```powershell
git clone <your-github-repo-url> EyeScan_Shared_Repo
```

## Daily workflow

On the machine that made changes:

```bash
git add EyeScan_Shared
git commit -m "Update EyeScan handoff"
git push
```

On the other machine:

```bash
git pull
```

## Important rule

Local Codex reads local files on its own machine. GitHub is the sync point, not the live filesystem that Codex reads directly.

## Recommended use

- keep docs and metadata in Git
- keep very large model files outside Git unless Git LFS is set up
- record large artifact paths and evaluation notes in the docs

