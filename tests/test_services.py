from app.services.ats_engine import extract_job_skills, score_cv_against_job
from app.services.recommendation_engine import get_learning_recommendations


def test_extract_job_skills_and_score():
    description = "We need experience with Python, FastAPI and Docker."

    job_skills = extract_job_skills(description)
    assert "python" in [s.lower() for s in job_skills]
    assert "fastapi" in [s.lower() for s in job_skills]
    assert "docker" in [s.lower() for s in job_skills]

    # CV has python and docker only
    cv_skills = ["python", "docker"]

    result = score_cv_against_job(cv_skills, job_skills)
    assert isinstance(result, dict)
    assert result["score"] in (0, 33, 50, 66, 100) or 0 <= result["score"] <= 100
    assert "kubernetes" not in result["missing_skills"]


def test_get_learning_recommendations_for_missing_skill():
    missing = ["Docker"]
    recs = get_learning_recommendations(missing)
    assert isinstance(recs, list)
    assert any(r["skill"].lower() == "docker" for r in recs)
