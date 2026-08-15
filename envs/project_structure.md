TechCareerFit — Project structure & modules

This file explains the repository layout and the purpose of the main modules. Place it with other environment files for quick developer onboarding.

Top-level layout

```
techcareerfit-backend/
├── alembic/               # DB migration settings and revisions
├── app/                   # FastAPI application code (main application package)
│   ├── api/               # HTTP routers (endpoints)
│   ├── core/              # app-wide configuration, DB connection, security
│   ├── models/            # SQLAlchemy ORM models (tables)
│   ├── schemas/           # Pydantic request/response models
│   ├── services/          # Business logic (CV parsing, ATS scoring, recommendations)
│   └── main.py            # FastAPI app factory / router wiring
├── tests/                 # Unit / integration tests
├── envs/                  # Example envs and onboarding docs (this folder)
├── requirements.txt       # Python deps
├── README.md              # Project README & quickstart
└── alembic.ini            # Alembic config
```

Short module descriptions

- `app/api/` — Contains routers exposed by the API. Examples:
  - `auth.py` — register/login/password-reset
  - `cv.py` — upload, parse, list, delete CVs (uses Supabase storage)
  - `ats.py` — job creation and ATS analysis endpoints
  - `applications.py` — create/list/update/delete job applications
  - `admin.py` — admin management endpoints (users, jobs, CVs, reports)

- `app/core/` — Core infrastructure and helpers:
  - `config.py` loads settings from environment / `.env`
  - `database.py` SQLAlchemy engine, session, Base
  - `security.py` password hashing, JWT utilities, current-user dependency
  - `storage.py` Supabase storage client wrapper

- `app/models/` — SQLAlchemy ORM models that map to DB tables (User, CV, JobDescription, Application, ATSResult, etc.). When you change models, create an Alembic revision.

- `app/schemas/` — Pydantic models used for request validation and response serialization. Keep these decoupled from ORM models where helpful.

- `app/services/` — Core business logic separated from HTTP layer:
  - `cv_parser.py` — extract text from PDF/DOCX and parse into structured fields; OCR fallback via `pytesseract` if needed
  - `ats_engine.py` — extract job skills, score CVs against job descriptions
  - `recommendation_engine.py` — map missing skills to learning resources

- `app/api/reports.py` — report endpoints and download support (JSON attachment; PDF generation can be added).

Developer notes

- Add new DB columns/tables using Alembic:
  ```bash
  alembic revision --autogenerate -m "describe change"
  alembic upgrade head
  ```
- To run tests locally:
  ```bash
  set PYTHONPATH=. && myenv\Scripts\python -m pytest -q
  ```
- Required environment variables are documented in `envs/.env.example` — copy to `.env` and fill values.

If you want this as an onboarding README in a different location, tell me where to move it.
