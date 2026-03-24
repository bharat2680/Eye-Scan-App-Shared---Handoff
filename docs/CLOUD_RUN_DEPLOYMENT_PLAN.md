# EyeScan Cloud Run Deployment Plan

Last updated: 2026-03-24 11:30 AEDT

## Goal

Move EyeScan off the Mac LAN backend and onto a public HTTPS backend so Android
and iPhone testers can receive live screening results outside the local Wi-Fi
network.

## What is already prepared locally

- backend runtime folder:
  `/Users/bharatsharma/FlutterProjects/eye_scan_app/backend`
- Cloud Run container scaffold added locally:
  - `backend/Dockerfile`
  - `backend/.dockerignore`
- backend quality gate is now self-contained for deployment:
  - bundled local quality model:
    `backend/model_assets/anterior_quality_gate_v1/model.keras`
- backend model packages already present locally:
  - `anterior_surface_binary_v2_simplecnn_package`
  - `anterior_cataract_vs_normal_v1_simplecnn_package`
  - `anterior_conjunctivitis_vs_normal_v1_simplecnn_package`
  - `anterior_uveitis_vs_normal_v1_simplecnn_package`
  - `anterior_pterygium_vs_normal_v1_simplecnn_package`
  - `eye_vs_non_eye_gate_v1_simplecnn_package`
- backend dependencies updated locally for deployment:
  - `gunicorn==23.0.0`
  - `tensorflow-cpu==2.20.0`

## Recommended first deployment shape

Use **Google Cloud Run** first, with a public HTTPS endpoint.

Recommended beta service profile:

- service name:
  `eyescan-backend-beta`
- region:
  `australia-southeast2`
- CPU:
  `2`
- memory:
  `4Gi`
- concurrency:
  `1`
- timeout:
  `300s`

This keeps the first public deployment simple and maintainable while we still
iterate on the model pipeline.

## Important current caveat

The backend still uses:

- SQLite for research metadata
- local upload storage under `pilot_uploads`

That is acceptable for a **beta inference deployment** only if we treat the
research upload path as non-durable. Cloud Run storage is ephemeral, so the
proper long-term production shape is:

- Cloud Run: API + inference
- Cloud Storage: uploads / persistent files
- Cloud SQL: durable metadata
- Secret Manager: secrets

## Suggested deployment command

Run this tomorrow after Google Cloud auth and project selection are ready:

```bash
gcloud config set project YOUR_PROJECT_ID
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com

gcloud run deploy eyescan-backend-beta \
  --source /Users/bharatsharma/FlutterProjects/eye_scan_app/backend \
  --region australia-southeast2 \
  --allow-unauthenticated \
  --cpu 2 \
  --memory 4Gi \
  --concurrency 1 \
  --timeout 300
```

## Immediate validation after deploy

Once Cloud Run returns the service URL:

```bash
curl https://YOUR_SERVICE_URL/health
curl https://YOUR_SERVICE_URL/models/current
```

Expected:

- `status: ok`
- `model_version: anterior_screening_eval_v7`
- `eye_presence_model_available: true`

## Mobile follow-up after deploy

### Internal beta

- runtime backend entry is now the fallback path for release builds that do not
  include a compiled backend URL
- beta testers can open Settings, save the public backend URL, and test without
  receiving fake `0%` placeholder results

### Real release

After the Cloud Run URL is stable, the correct release path is:

- compile `EYESCAN_BACKEND_URL=https://YOUR_SERVICE_URL`
- rebuild Android and iOS release builds

## Remaining deployment blockers

Not code blockers anymore:

- Google Cloud auth / account access
- project selection
- API enablement

Still architectural work for later:

- Cloud SQL migration
- Cloud Storage migration
- clinic-level auth / quotas / trial enforcement
