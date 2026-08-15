from typing import List, Dict


LEARNING_RESOURCES = {

    "python": [
        {
            "title": "Python Documentation",
            "provider": "Python",
            "url": "https://docs.python.org/3/tutorial/",
            "type": "Documentation",
            "level": "Beginner"
        }
    ],

    "fastapi": [
        {
            "title": "FastAPI Documentation",
            "provider": "FastAPI",
            "url": "https://fastapi.tiangolo.com/",
            "type": "Documentation",
            "level": "Intermediate"
        }
    ],

    "docker": [
        {
            "title": "Docker Get Started",
            "provider": "Docker",
            "url": "https://docs.docker.com/get-started/",
            "type": "Tutorial",
            "level": "Beginner"
        }
    ],

    "kubernetes": [
        {
            "title": "Kubernetes Basics",
            "provider": "Kubernetes",
            "url": "https://kubernetes.io/docs/tutorials/kubernetes-basics/",
            "type": "Tutorial",
            "level": "Intermediate"
        }
    ],

    "rest apis": [
        {
            "title": "REST API Concepts",
            "provider": "MDN",
            "url": "https://developer.mozilla.org/en-US/docs/Glossary/REST",
            "type": "Documentation",
            "level": "Beginner"
        }
    ],

    "javascript": [
        {
            "title": "JavaScript Guide",
            "provider": "MDN",
            "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide",
            "type": "Documentation",
            "level": "Beginner"
        }
    ],

    "react": [
        {
            "title": "React Documentation",
            "provider": "React",
            "url": "https://react.dev/learn",
            "type": "Tutorial",
            "level": "Beginner"
        }
    ],

    "sql": [
        {
            "title": "SQL Tutorial",
            "provider": "W3Schools",
            "url": "https://www.w3schools.com/sql/",
            "type": "Tutorial",
            "level": "Beginner"
        }
    ],

    "postgresql": [
        {
            "title": "PostgreSQL Documentation",
            "provider": "PostgreSQL",
            "url": "https://www.postgresql.org/docs/",
            "type": "Documentation",
            "level": "Intermediate"
        }
    ],

    "git": [
        {
            "title": "Git Documentation",
            "provider": "Git",
            "url": "https://git-scm.com/doc",
            "type": "Documentation",
            "level": "Beginner"
        }
    ],

    "linux": [
        {
            "title": "Linux Documentation",
            "provider": "Linux",
            "url": "https://www.linux.org/",
            "type": "Documentation",
            "level": "Beginner"
        }
    ],

    "aws": [
        {
            "title": "AWS Training and Certification",
            "provider": "AWS",
            "url": "https://aws.amazon.com/training/",
            "type": "Training",
            "level": "Beginner"
        }
    ],

    "microsoft azure": [
        {
            "title": "Microsoft Learn - Azure",
            "provider": "Microsoft",
            "url": "https://learn.microsoft.com/en-us/training/azure/",
            "type": "Training",
            "level": "Beginner"
        }
    ],

    "machine learning": [
        {
            "title": "Machine Learning Resources",
            "provider": "Google",
            "url": "https://developers.google.com/machine-learning",
            "type": "Training",
            "level": "Intermediate"
        }
    ],

    "cybersecurity": [
        {
            "title": "Cybersecurity Learning",
            "provider": "Cisco",
            "url": "https://www.cisco.com/c/en/us/training-events/training-certifications/training/courses/cybersecurity.html",
            "type": "Training",
            "level": "Beginner"
        }
    ],
}


def get_learning_recommendations(
    missing_skills: List[str]
) -> List[Dict]:

    recommendations = []

    for skill in missing_skills:

        skill_key = skill.strip().lower()

        resources = LEARNING_RESOURCES.get(skill_key, [])

        for resource in resources:

            recommendations.append({
                "skill": skill,
                "title": resource["title"],
                "provider": resource["provider"],
                "url": resource["url"],
                "type": resource["type"],
                "level": resource["level"]
            })

    return recommendations