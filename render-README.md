# Deploying TechCareerFit to Render (Docker)

Overview
- This project requires system packages for OCR and PDF parsing (`tesseract-ocr`, `poppler-utils`). Use Render's Docker service so these can be installed in the image.

Files added
- `Dockerfile` — builds the app, installs system deps, runs `alembic upgrade head`, then starts `uvicorn`.
- `.dockerignore` — excludes local venv, secrets and tests from the image.

Render setup
1. On Render, create a new **Web Service** and choose **Docker** as the environment.
2. Connect your GitHub repo and select branch (e.g. `main`).

Environment variables (set in Render Dashboard → Environment)
- `DATABASE_URL` — Postgres connection string (Render Postgres or Supabase/Postgres).
- `JWT_SECRET_KEY` — your JWT signing secret.
- `SUPABASE_URL` and `SUPABASE_KEY` — if using Supabase for CV storage.
- `TESSERACT_CMD` — optional (default `/usr/bin/tesseract`).
- Any other app-specific envs from your local `.env` (do NOT commit `.env`).

Build & start
- Render will build the Dockerfile. The container runs this command:
  `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}`

Health check
- Set the health check path to `/` or `/health` if you expose one.

Notes
- Do NOT store secrets in the repository. Use Render's Environment settings.
- Render's filesystem is ephemeral; use Supabase (or another object store) for uploaded CVs.
- If you prefer not to use Docker, you can use a Render Python service but you'll lose easy installation of system packages needed for OCR.

Local build & test
```bash
# build
docker build -t techcareerfit:local .

# run (replace envs as necessary)
docker run -e DATABASE_URL="postgres://..." -e SUPABASE_URL="..." -e SUPABASE_KEY="..." -p 10000:10000 techcareerfit:local
```
