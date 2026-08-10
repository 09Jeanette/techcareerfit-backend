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
- Upload CVs
- Parse PDF and DOCX files
- Store CV metadata

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
- Passlib (Bcrypt) — see [Known Issues](#known-issues--troubleshooting) for a required version pin

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

> **Note:** `requirements.txt` pins `bcrypt==4.0.1`. This is required — see [Known Issues](#known-issues--troubleshooting) below before changing it.

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

### Via curl

1. Start the server:

```bash
uvicorn app.main:app --reload
```

2. Register a user:

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"full_name":"John Doe","email":"johndoe@example.com","password":"Password123"}'
```

3. Login and capture the token:

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"johndoe@example.com","password":"Password123"}'
```

4. Request a password reset token:

```bash
curl -X POST http://127.0.0.1:8000/auth/password-reset/request \
  -H "Content-Type: application/json" \
  -d '{"email":"johndoe@example.com"}'
```

5. Confirm a new password using the returned reset token:

```bash
curl -X POST http://127.0.0.1:8000/auth/password-reset/confirm \
  -H "Content-Type: application/json" \
  -d '{"reset_token":"<jwt>","new_password":"NewPassword456"}'
```

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

#### GET /cv/

```json
{
  "message": "CV endpoint"
}
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

## Known Issues / Troubleshooting

### `AttributeError: module 'bcrypt' has no attribute '__about__'` / `password cannot be longer than 72 bytes`

This occurs on `/auth/register` and `/auth/login` because `passlib` (last released in 2020) checks for a `bcrypt.__about__.__version__` attribute that was removed in `bcrypt` 4.1+. Passlib's fallback version-detection routine then fails in a way that surfaces as a `ValueError` about password length, even though your actual password is nowhere near 72 bytes.

**Fix:**

```bash
pip uninstall bcrypt -y
pip install bcrypt==4.0.1
```

Make sure `requirements.txt` pins this version so it doesn't regress on a fresh install:

```text
bcrypt==4.0.1
```

Restart the server after reinstalling.

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