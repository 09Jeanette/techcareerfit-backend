ATS (Jobs & Analysis)

1) Create Job

-- POST `{{base_url}}/ats/jobs` — Body:

```json
{
  "title": "Backend Developer",
  "company": "TechCorp",
  "description": "Experience with Python, FastAPI, PostgreSQL, Docker"
}
```

2) Analyze

-- POST `{{base_url}}/ats/analyze` — Body:

```json
{
  "cv_id": "<uuid-of-cv>",
  "job_id": "<uuid-of-job>"
}
```
-- Response: ATS result object with `score`, `missing_skills`, `recommendations`, and `learning_resources`.

Example response:

```json
{
  "id":"...",
  "cv_id":"...",
  "job_id":"...",
  "score": 65,
  "missing_skills": ["Docker","Kubernetes"],
  "recommendations": ["Consider adding or highlighting experience with: Docker","Consider adding or highlighting experience with: Kubernetes"],
  "learning_resources": [
    {"skill":"Docker","title":"Docker Get Started","provider":"Docker","url":"https://docs.docker.com/get-started/","type":"Tutorial","level":"Beginner"},
    {"skill":"Kubernetes","title":"Kubernetes Basics","provider":"Kubernetes","url":"https://kubernetes.io/docs/tutorials/kubernetes-basics/","type":"Tutorial","level":"Intermediate"}
  ]
}
```

Report guidance:

- "What went well": skills matched between CV and job description (higher score contributors).
- "What went wrong": missing skills detected in the job description that are not present in the CV.
- "How to improve": `learning_resources` contains actionable course/tutorial links for each missing skill — include these on the CV and re-analyze to increase your score.
Applications (Application Tracking)

The application tracker records applications and supports richer fields to help you learn from each submission. Stored fields include:

- `company`, `position`, `status` (applied/interview/offer/rejected), `applied_date`
- `job_description` — the job description text submitted by the employer
- `date_posted` — when the job was posted (optional)
- `cv_id` — which uploaded CV was used for this application (helps compare outcomes across CVs)
- `ats_score` — ATS compatibility score for the CV vs job (if you run the analyzer)
- `comments` — notes or feedback about the application

1) Create Application

- POST `{{base_url}}/applications/` — Body:

```json
{
  "company": "TechCorp",
  "position": "Backend Engineer",
  "status": "applied",
  "applied_date": "2026-08-01",
  "job_description": "Looking for Python, FastAPI, Docker",
  "date_posted": "2026-07-20",
  "cv_id": "<uuid-of-cv>",
  "ats_score": 65,
  "comments": "Applied via company portal"
}
```

2) List Applications

- GET `{{base_url}}/applications/` — returns applications for the authenticated user.

3) Get / Update / Delete Application

- GET `{{base_url}}/applications/{application_id}`
- PUT `{{base_url}}/applications/{application_id}` (same body as create)
- DELETE `{{base_url}}/applications/{application_id}`

Use the `cv_id` and `ats_score` fields to compare which CVs and changes led to better ATS compatibility and interview outcomes.
# TechCareerFit Backend

TechCareerFit is a web-based ATS Compatibility, Skills Gap Analysis, and Career Development Platform designed for ICT students, graduates, and technology professionals.

The backend is built with FastAPI and PostgreSQL and provides authentication, CV management, ATS scoring, skills gap analysis, learning recommendations, job application tracking, and report generation.

---

## Features

### Authentication
- User Registration
- User Login
- JWT Authentication
- Password Hashing with Bcrypt
- Password Reset (Request + Confirm)

### CV Management
- Upload CVs (PDF/DOCX) to Supabase Storage, scoped to the authenticated user
- List, retrieve, and delete a user's own CVs
- Store CV metadata in PostgreSQL
- All CV endpoints require a valid JWT (`Authorization: Bearer <token>`)

### ATS Compatibility Analysis
- Compare CVs against job descriptions
- ATS Compatibility Score
- Missing Skills Identification

### Career Development
- Learning Recommendations
- Skill Gap Analysis
- Technology Career Roadmaps

### Job Application Tracking
- Track applications
- Track interview status
- Track offers and rejections

### Reporting
- ATS Report Generation
- PDF Export

---

## Tech Stack

### Backend

- FastAPI
- Python 3.12+
- SQLAlchemy
- Alembic

### Database

- PostgreSQL
- Supabase

### Authentication

- JWT (python-jose)
- Passlib (Bcrypt), pinned to `bcrypt==4.0.1`

### NLP & ATS Analysis

- spaCy
- Sentence Transformers

### Version Control

- Git
- GitHub

---

## Project Structure

```text
techcareerfit-backend/

├── app/
│
├── api/
│   ├── auth.py
│   ├── users.py
│   ├── cv.py
│   ├── ats.py
│   ├── jobs.py
│   └── reports.py
│
├── core/
│   ├── config.py
│   ├── database.py
│   └── security.py
│
├── models/
│   ├── user.py
│   ├── cv.py
│   ├── job.py
│   ├── application.py
│   └── ats_result.py
│
├── schemas/
│   └── auth.py
│
├── services/
│
├── utils/
│
├── uploads/
│
├── tests/
│
├── alembic/
│
├── main.py
│
├── requirements.txt
├── .env
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/techcareerfit-backend.git

cd techcareerfit-backend
```

### Create Virtual Environment

Windows

```bash
python -m venv myenv
```

Activate

```bash
myenv\Scripts\activate
```

Linux / Mac

```bash
python3 -m venv myenv

source myenv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** `requirements.txt` pins `bcrypt==4.0.1`.

---

### Apply Database Migrations

After installing dependencies and setting up `.env`, sync the database schema with the models:

```bash
alembic upgrade head
```

Whenever a model under `app/models/` changes (new column, new table, etc.), generate and apply a new migration rather than editing the database by hand:

```bash
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```

Skipping this step can cause `UndefinedColumn` errors at runtime if the live table falls out of sync with the models.

---

## Environment Variables

Create a `.env` file in the project root.

```env
DATABASE_URL=postgresql://postgres.auooomxpnxwsmwuihkgb:PASSWORD@aws-0-eu-west-3.pooler.supabase.com:6543/postgres

JWT_SECRET_KEY=techcareerfit_secret

JWT_ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## Run Application

```bash
uvicorn app.main:app --reload
```

Server:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc Documentation:

```text
http://127.0.0.1:8000/redoc
```

---

## API Endpoints

### Root

#### GET /

Response

```json
{
  "message": "Welcome to TechCareerFit API"
}
```

---

### Authentication

#### GET /auth/

Response

```json
{
  "message": "Auth module running"
}
```

#### POST /auth/register

Request

```json
{
  "full_name": "John Doe",
  "email": "johndoe@example.com",
  "password": "Password123"
}
```

Response

```json
{
  "message": "User registered successfully"
}
```

Returns `400 Bad Request` if the email is already registered.

---

#### POST /auth/login

Request

```json
{
  "email": "johndoe@example.com",
  "password": "Password123"
}
```

Response

```json
{
  "message": "Login successful",
  "access_token": "<jwt>",
  "token_type": "bearer",
  "email": "johndoe@example.com"
}
```

Returns `401 Unauthorized` for an invalid email or password.

---

#### POST /auth/password-reset/request

Request

```json
{
  "email": "johndoe@example.com"
}
```

Response

```json
{
  "message": "Password reset token generated",
  "reset_token": "<jwt>",
  "note": "In production, send this token to the user by email."
}
```

If the email does not exist, the endpoint still returns `200` with a generic message and no token, so as not to reveal which emails are registered.

---

#### POST /auth/password-reset/confirm

Request

```json
{
  "reset_token": "<jwt>",
  "new_password": "NewPassword123"
}
```

Response

```json
{
  "message": "Password has been reset successfully"
}
```

Returns `400 Bad Request` if the reset token is invalid or expired.

---

## Authentication Testing

### Via Postman

Create a collection called **TechCareerFit Auth** with a collection variable `base_url = http://127.0.0.1:8000`, then add requests using `{{base_url}}/auth/...`.

| # | Method | Endpoint | Body | Expected |
|---|--------|----------|------|----------|
| 1 | POST | `/auth/register` | `{"full_name":"John Doe","email":"johndoe@example.com","password":"Password123"}` | `200` — user registered |
| 1b | POST | `/auth/register` | same as above (repeat) | `400` — email already registered |
| 2 | POST | `/auth/login` | `{"email":"johndoe@example.com","password":"Password123"}` | `200` — `access_token` returned |
| 2b | POST | `/auth/login` | `{"email":"johndoe@example.com","password":"WrongPassword"}` | `401` — invalid credentials |
| 3 | POST | `/auth/password-reset/request` | `{"email":"johndoe@example.com"}` | `200` — `reset_token` returned |
| 3b | POST | `/auth/password-reset/request` | `{"email":"notjohndoe@example.com"}` | `200` — generic message, no token |
| 4 | POST | `/auth/password-reset/confirm` | `{"reset_token":"<paste from step 3>","new_password":"NewPassword456"}` | `200` — password reset |
| 4b | POST | `/auth/login` | `{"email":"johndoe@example.com","password":"NewPassword456"}` | `200` — confirms new password works |
| 4c | POST | `/auth/login` | `{"email":"johndoe@example.com","password":"Password123"}` | `401` — confirms old password no longer works |

Tip: on the login request's **Tests** tab, save the token automatically for reuse in later requests:

```javascript
pm.collectionVariables.set("access_token", pm.response.json().access_token);
```

---

### Users

#### GET /users/

```json
{
  "message": "Users endpoint"
}
```

---

### CV

All `/cv/*` endpoints require a valid access token: `Authorization: Bearer <token>`. Results are scoped to the authenticated user — you can only see, fetch, or delete your own CVs.

#### POST /cv/upload

Multipart form-data request, field name `file` (PDF or DOCX only).

Response

```json
{
  "id": "c0ae4cc7-9cab-47fc-9586-b40291a62a5d",
  "message": "CV uploaded successfully",
  "file_name": "Jeanette_Kgabe_CV.docx",
  "file_url": "075facc1-b466-4fb5-a92d-e2321728ac27.docx"
}
```

Returns `400 Bad Request` for a non-PDF/DOCX file, `401 Unauthorized` without a valid token.

---

#### GET /cv/

Response: array of the authenticated user's CVs.

---

#### GET /cv/{cv_id}

Response: a single CV's details. Returns `404 Not Found` if the CV doesn't exist or doesn't belong to the authenticated user.

---

#### DELETE /cv/{cv_id}

Response

```json
{
  "message": "CV deleted successfully"
}
```

Removes the file from Supabase Storage and the row from the database. Returns `404 Not Found` if the CV doesn't exist or doesn't belong to the authenticated user.

---

### CV Testing (Postman)

Prerequisite: log in via `/auth/login` and save `access_token` as a collection variable (see Authentication Testing above).

| # | Method | Endpoint | Auth | Body | Expected |
|---|--------|----------|------|------|----------|
| 1 | POST | `/cv/upload` | Bearer `{{access_token}}` | form-data, key `file` (type **File**), pick a `.pdf`/`.docx` | `200` — id, file_name, file_url |
| 1b | POST | `/cv/upload` | Bearer `{{access_token}}` | form-data, `.jpg` | `400` — invalid extension |
| 1c | POST | `/cv/upload` | none | same `.pdf` | `401` — unauthorized |
| 2 | GET | `/cv/` | Bearer `{{access_token}}` | — | `200` — array of your CVs |
| 3 | GET | `/cv/{{cv_id}}` | Bearer `{{access_token}}` | — | `200` — CV details |
| 3b | GET | `/cv/00000000-0000-0000-0000-000000000000` | Bearer `{{access_token}}` | — | `404` |
| 4 | DELETE | `/cv/{{cv_id}}` | Bearer `{{access_token}}` | — | `200` — deleted |
| 4b | GET | `/cv/{{cv_id}}` (repeat) | Bearer `{{access_token}}` | — | `404` — confirms deletion |

On the upload request's **Tests** tab, save the returned id for reuse:

```javascript
pm.collectionVariables.set("cv_id", pm.response.json().id);
```

---

### ATS

#### GET /ats/

```json
{
  "message": "ATS engine endpoint"
}
```

---

### Jobs

#### GET /jobs/

```json
{
  "message": "Jobs endpoint"
}
```

---

### Reports

#### GET /reports/

```json
{
  "message": "Reports endpoint"
}
```

---

## Development Workflow

### Main Branches

```text
main
develop
```

### Feature Branches

```text
feature/authentication
feature/cv-upload
feature/cv-parser
feature/ats-engine
feature/skills-gap-analysis
feature/recommendations
feature/job-tracking
feature/pdf-reports
```

### Workflow

```text
feature/*
    ↓
develop
    ↓
main
```

---

## Database Tables

### users

```text
id
full_name
email
password_hash
role
created_at
```

### cvs

```text
id
user_id
file_name
file_url
uploaded_at
```


### Parse CV

#### POST /cv/{cv_id}/parse

Parses an uploaded PDF or DOCX CV and extracts its textual content.

The endpoint:

- Downloads the file from Supabase Storage
- Detects whether the file is a PDF or DOCX
- Extracts text from the document
- Stores the extracted text in the `parsed_text` column of the `cvs` table
- Returns parsing statistics

**Authentication Required**

```http
Authorization: Bearer <token>
```

**Request**

```http
POST /cv/{cv_id}/parse
```

Example:

```http
POST /cv/31b2dd10-ed68-426f-aed0-32562746dd23/parse
```

**Response**

```json
{
  "message": "CV parsed successfully",
  "characters": 5420
}
```

Where:

- `message` indicates successful parsing.
- `characters` is the total number of characters extracted from the CV.

---

#### GET /cv/{cv_id}/parsed

Returns the parsed content stored for the CV.

**Authentication Required**

```http
Authorization: Bearer <token>
```

**Request**

```http
GET /cv/{cv_id}/parsed
```

Example:

```http
GET /cv/31b2dd10-ed68-426f-aed0-32562746dd23/parsed
```

**Response**

```json
{
  "id": "31b2dd10-ed68-426f-aed0-32562746dd23",
  "file_name": "Jeanette_Kgabe_CV.pdf",
  "parsed_text": "Jeanette Kgabe\nSoftware Developer\nPython\nFastAPI\nPostgreSQL..."
}
```

---

### CV Parser Testing (Postman)

Prerequisites:

1. Register a user
2. Log in
3. Upload a CV
4. Save the returned `cv_id`

| Step | Endpoint | Expected Result |
|--------|----------|----------|
| Upload CV | `POST /cv/upload` | CV saved successfully |
| Parse CV | `POST /cv/{cv_id}/parse` | Text extracted and stored |
| View Parsed Text | `GET /cv/{cv_id}/parsed` | Parsed CV text returned |

---

### Supported Formats

The parser currently supports:

```text
PDF (.pdf)
DOCX (.docx)
```

Files uploaded in any other format will result in:

```json
{
  "detail": "Unsupported file type"
}
```

---

### Database Changes

The `cvs` table has been extended to include:

```text
parsed_text
```

This field stores the extracted text from the uploaded CV and serves as the foundation for:

- ATS Compatibility Scoring
- Skills Gap Analysis
- Learning Recommendations
- Career Roadmap Generation

---


# ATS Engine

The **Applicant Tracking System (ATS) Engine** evaluates how well a candidate's CV matches the requirements of a specific job description.

The engine uses the parsed CV content together with the selected job description to generate an **ATS compatibility score**, identify **missing skills**, and provide **recommendations** to improve the candidate's CV alignment with the position.

### ATS Analysis Workflow

```text
Uploaded CV
     │
     ▼
CV Text Extraction
     │
     ▼
Parsed CV Content
     │
     ├──────────────┐
     │              │
     ▼              ▼
Job Description   CV Content
     │              │
     └──────┬───────┘
            ▼
      ATS Analysis Engine
            │
            ▼
    Compatibility Score
            │
       ┌────┴─────┐
       ▼          ▼
Missing Skills  Recommendations
```

### Job Descriptions

#### POST /ats/jobs

Creates a new job description for the authenticated user.

**Request**

```json
{
  "title": "Backend Developer",
  "company": "TechCorp",
  "description": "Looking for experience in Python, FastAPI, SQL, and Docker."
}
```

**Response**

The created job description is stored and can subsequently be used for CV analysis.

---

#### GET /ats/jobs

Returns the job descriptions associated with the authenticated user.

---

### CV Analysis

#### POST /ats/analyze

Analyzes a CV against a selected job description.

Both the CV and job description must already exist in the system.

**Request**

```json
{
  "cv_id": "uuid-of-cv",
  "job_id": "uuid-of-job"
}
```

**Analysis Output**

The ATS engine returns an analysis result containing:

* **ATS Compatibility Score** — indicates how closely the CV matches the selected job description.
* **Missing Skills** — identifies skills referenced by the job description that are not sufficiently represented in the CV.
* **Recommendations** — provides suggestions for improving the CV's alignment with the job requirements.

**Example Response**

```json
{
  "id": "uuid",
  "cv_id": "uuid-of-cv",
  "job_id": "uuid-of-job",
  "score": 75,
  "missing_skills": [
    "Docker"
  ],
  "recommendations": [
    "Consider adding or highlighting experience with: Docker"
  ]
}
```

### Analysis Results

#### GET /ats/results

Returns the ATS analysis results belonging to the authenticated user.

Each result links:

* The analyzed CV
* The selected job description
* The ATS compatibility score
* Identified missing skills
* Generated recommendations

### Authentication

All ATS endpoints require a valid JWT access token.

```http
Authorization: Bearer <token>
```

ATS data is scoped to the authenticated user to ensure that users can only access their own job descriptions and analysis results.

### ATS Engine Status

The ATS Engine is currently implemented and operational.

```text
CV Parsing
    ↓
Job Description Creation
    ↓
CV + Job Matching
    ↓
ATS Compatibility Score
    ↓
Missing Skills Detection
    ↓
Recommendations
    ↓
Analysis Result
```


### Current Development Status

✅ Authentication

✅ Password Reset

✅ JWT Authorization

✅ CV Upload (Supabase Storage)

✅ CV Retrieval & Deletion

✅ CV Text Extraction (PDF/DOCX)

✅ ATS Engine

🔜 Skills Gap Analysis

🔜 Learning Recommendations

🔜 Job Application Tracking

🔜 PDF Report Generation


**Quick Test Flow**

Prereqs: server running (`uvicorn app.main:app --reload`) and .env configured. Use Postman or curl. Add header `Authorization: Bearer <access_token>` for protected endpoints.

1) Register  
- POST `/auth/register`  
- Body JSON:
  - {"full_name":"Jane Student","email":"jane@example.com","password":"Password123!"}

2) Login (save token)  
- POST `/auth/login`  
- Body JSON:
  - {"email":"jane@example.com","password":"Password123!"}  
- Response contains `access_token`. In Postman save it as `access_token` and set Authorization = Bearer {{access_token}}.

3) Verify user  
- GET `/users/me` (Auth header must be set)

4) Upload CV  
- POST `/cv/upload` (Auth)  
- Body: form-data key `file` -> pick `.pdf` or `.docx`  
- Response returns `id` (`cv_id`) and `file_url`.

5) Parse CV  
- POST `/cv/{cv_id}/parse` (Auth)  
- Response: `parsed_data` with `skills`, `email`, `phone`, `sections`. If PDF is scanned, OCR runs only if `pytesseract` + Tesseract are available.

6) View parsed text  
- GET `/cv/{cv_id}/parsed` (Auth)

7) Create job description  
- POST `/ats/jobs` (Auth)  
- Body JSON:
  - {"title":"Backend Developer","company":"TechCorp","description":"Python, FastAPI, PostgreSQL, Docker"}

8) Analyze CV vs job  
- POST `/ats/analyze` (Auth)  
- Body JSON:
  - {"cv_id":"<cv_id>","job_id":"<job_id>"}  
- Response: `score`, `missing_skills`, `recommendations`. Save ATS result if needed.

9) List ATS results  
- GET `/ats/results` (Auth)

10) Skills-gap analysis  
- POST `/skills-gap/analyze` (Auth)  
- Body JSON:
  - {"cv_id":"<cv_id>","roadmap":"backend-development"}  
- Response: `matched_skills`, `missing_skills`, `match_percentage`, `recommended_learning`.

11) Learning recommendations (by missing skills)  
- POST `/recommendations/learning` (Auth)  
- Body JSON:
  - {"missing_skills":["Docker","Kubernetes","REST APIs"]}

12) Application tracking (CRUD)  
- Create: POST `/applications/` (Auth) Body:
  - {"company":"TechCorp","position":"Backend Engineer","status":"applied","applied_date":"2026-08-01"}  
- List: GET `/applications/`  
- Get: GET `/applications/{application_id}`  
- Update: PUT `/applications/{application_id}` (same body shape)  
- Delete: DELETE `/applications/{application_id}`

13) Reports (scaffold)  
- GET `/reports/` (Auth) — see available report endpoints later.

Postman tips:
- Use a collection variable `base_url = http://127.0.0.1:8000`.  
- Add a Test script on the login request:
  - `pm.collectionVariables.set("access_token", pm.response.json().access_token);`  
- Use `Authorization: Bearer {{access_token}}` for saved requests.

If you want, I can:
- Generate a Postman collection JSON for these requests, or  
- Add starter pytest tests for register/login, upload+parse, and ATS analyze. Which should I do next?