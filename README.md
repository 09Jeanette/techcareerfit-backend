# ATS Application — Final Test Run Guide

## 1. Application Overview

### Purpose

The application provides:

* CV management
* CV parsing
* ATS compatibility scoring
* Skills-gap recommendations
* Learning-resource recommendations
* Job management
* Job application tracking
* ATS report generation and downloads
* Administrative user, CV, job, and report management

### Main Flow

```text
Authentication
     ↓
Upload CV
     ↓
Parse CV
     ↓
Create Job
     ↓
ATS Analysis
     ↓
Score + Missing Skills + Recommendations
     ↓
Generate Report
     ↓
Track Job Application
```

---

# 2. Environment Setup

## 2.1 Apply Database Migrations

```bash
alembic upgrade head
```

## 2.2 Start the Development Server

```bash
uvicorn app.main:app --reload
```

The API will normally be available at:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

## 2.3 Run Unit Tests

Windows:

```bash
set PYTHONPATH=. && myenv\Scripts\python -m pytest -q
```

If imports fail, ensure that the project root is included in `PYTHONPATH`.

---

# 3. Authentication Module

Authentication uses JWT tokens.

## 3.1 Register

Registration is optional if an account already exists.

### Endpoint

```http
POST /auth/register
```

### Request Body

```json
{
  "full_name": "Jane Example",
  "email": "jane@example.com",
  "password": "Password123!"
}
```

---

## 3.2 Login

### Endpoint

```http
POST /auth/login
```

### Request Body

```json
{
  "email": "jane@example.com",
  "password": "Password123!"
}
```

### Expected Result

The response should contain an:

```text
access_token
```

Save the token and use it for authenticated requests.

### Authorization Header

```http
Authorization: Bearer <access_token>
```

---

# 4. CV Management Module

The CV module handles CV uploads, parsing, and retrieval.

## 4.1 Upload CV

### Endpoint

```http
POST /cv/upload
```

### Request

Use:

```text
multipart/form-data
```

with the file field:

```text
file
```

### Expected Result

The response should provide a:

```text
cv_id
```

Save the `cv_id` for the remaining CV and ATS tests.

---

## 4.2 Parse CV

### Endpoint

```http
POST /cv/{cv_id}/parse
```

Replace:

```text
{cv_id}
```

with the ID returned from the upload request.

### Expected Result

The response should contain:

```text
parsed_data
parsed_at
```

---

## 4.3 Admin Parsed CV View

### Endpoint

```http
GET /admin/cvs/{cv_id}/parsed
```

This endpoint is restricted to administrators.

---

# 5. Job & ATS Analysis Module

The ATS module compares a user's CV against a job description.

## 5.1 Create Job

### Endpoint

```http
POST /ats/jobs
```

### Request Body

```json
{
  "title": "Backend Developer",
  "company": "Acme",
  "description": "Python, FastAPI, Docker, PostgreSQL"
}
```

### Expected Result

The response should provide a:

```text
job_id
```

Save the `job_id`.

---

## 5.2 Analyze CV Against Job

### Endpoint

```http
POST /ats/analyze
```

### Request Body

```json
{
  "cv_id": "<cv_id>",
  "job_id": "<job_id>"
}
```

### Expected Result

The response should include:

* `score`
* `missing_skills`
* `recommendations`
* `learning_resources`

Example:

```json
{
  "score": 65,
  "missing_skills": [
    "Docker",
    "PostgreSQL"
  ],
  "recommendations": [
    "Improve Docker experience",
    "Add PostgreSQL projects"
  ],
  "learning_resources": []
}
```

---

# 6. Reports Module

The reports module provides downloadable ATS analysis reports.

## 6.1 Download ATS Report

### Endpoint

```http
GET /reports/{report_id}/download
```

### Access

The report can be downloaded by:

* The report owner
* An administrator

### Expected Response

The response should be an attachment.

Verify the:

```http
Content-Disposition
```

header contains:

```text
attachment; filename=report_<id>.json
```

---

# 7. Applications Module

The applications module allows users to track job applications and their outcomes.

## 7.1 Create Application — Job Link

### Endpoint

```http
POST /applications/
```

### Request Body

```json
{
  "company": "Acme",
  "position": "Backend Developer",
  "status": "applied",
  "applied_date": "2026-08-15",
  "job_description": "Looking for Python, FastAPI, Docker",
  "date_posted": "2026-08-10",
  "cv_id": "<cv_id>",
  "ats_score": 65,
  "comments": "Applied via website",
  "job_link": "https://acme.example/jobs/123"
}
```

---

## 7.2 Create Application — Email

Applications can also record applications submitted through email.

Include:

```json
{
  "application_email": "jobs@acme.example",
  "application_subject": "Application: Backend Developer - Jane Example"
}
```

These fields can be included together with the normal application information.

---

## 7.3 Verify Applications

### List Applications

```http
GET /applications/
```

### Get Individual Application

```http
GET /applications/{id}
```

### Update Application

```http
PUT /applications/{id}
```

### Delete Application

```http
DELETE /applications/{id}
```

Verify that each operation behaves as expected.

---

# 8. Administration Module

Administrative endpoints require an administrator account.

## 8.1 Promote User to Admin

### Endpoint

```http
POST /admin/users/{user_id}/promote
```

This endpoint is admin-only.

---

## 8.2 Create User

### Endpoint

```http
POST /admin/users/
```

### Request Body

```json
{
  "full_name": "Jane Example",
  "email": "jane@example.com",
  "password": "Password123!"
}
```

---

## 8.3 Suspend User

```http
POST /admin/users/{user_id}/suspend
```

---

## 8.4 Unsuspend User

```http
POST /admin/users/{user_id}/unsuspend
```

---

## 8.5 Download CV

### Endpoint

```http
GET /admin/cvs/{cv_id}/download
```

The original CV file should be returned as an attachment.

---

## 8.6 Manage Jobs

Administrative job management is available under:

```text
/admin/jobs/
```

Test the available list and delete operations.

---

## 8.7 Manage Reports

Administrative report management is available under:

```text
/admin/reports/
```

Test the available list and delete operations.

---

# 9. OCR Configuration

If CV parsing returns no text, the CV may require OCR.

Install the following Python packages:

```bash
pip install pytesseract Pillow
```

Tesseract OCR must also be installed as a system application.

After installation, ensure that the Tesseract executable is available to the application.

---

# 10. Supabase Storage

CV files are uploaded, downloaded, and deleted using Supabase storage.

Ensure the following environment variables are configured:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

Verify that:

* CV uploads work
* CV downloads work
* CV deletion works
* The stored file can be retrieved successfully

---

# 11. Admin Configuration

The application uses the user's role to determine administrative access.

A user can be made an administrator by setting:

```text
role = 'admin'
```

Alternatively, an existing administrator can use:

```http
POST /admin/users/{user_id}/promote
```

After promotion, verify that the user can access admin-only endpoints.

---

# 12. Final End-to-End Test Order

For the final test, execute the modules in this order:

### Step 1 — Environment

```bash
alembic upgrade head
```

```bash
uvicorn app.main:app --reload
```

### Step 2 — Automated Tests

```bash
set PYTHONPATH=. && myenv\Scripts\python -m pytest -q
```

### Step 3 — Authentication

* Register user
* Login
* Save JWT token
* Add Bearer token to authenticated requests

### Step 4 — CV

* Upload CV
* Save `cv_id`
* Parse CV
* Verify parsed data

### Step 5 — Job

* Create job
* Save `job_id`

### Step 6 — ATS

* Analyze CV against job
* Verify score
* Verify missing skills
* Verify recommendations
* Verify learning resources

### Step 7 — Reports

* Obtain report ID
* Download report
* Verify attachment filename

### Step 8 — Applications

* Create application
* View applications
* View individual application
* Update application
* Delete application

### Step 9 — Administration

* Promote user
* Create user
* Suspend user
* Unsuspend user
* Download CV
* Manage jobs
* Manage reports

### Step 10 — Storage & OCR

* Verify Supabase storage
* Test CV download/delete
* Test OCR with an image-based CV if required

---

# 13. Important Test Values

During testing, keep track of the following IDs:

```text
access_token = <JWT token>

cv_id = <uploaded CV ID>

job_id = <created job ID>

report_id = <generated report ID>

application_id = <created application ID>

user_id = <test user ID>
```

These IDs are reused throughout the end-to-end testing process.
