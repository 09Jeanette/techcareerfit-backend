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

- JWT
- Passlib (Bcrypt)

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
  "full_name": "Jeanette Kgabe",
  "email": "jeanette@example.com",
  "password": "Password123"
}
```

Response

```json
{
  "message": "User registered successfully"
}
```

---

#### POST /auth/login

Request

```json
{
  "email": "jeanette@example.com",
  "password": "Password123"
}
```

Response

```json
{
  "message": "Login successful"
}
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
