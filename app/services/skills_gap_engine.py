from typing import List, Dict


ROADMAP_SKILLS = {
    # Software Development
    "backend-development": [
        "Python",
        "Java",
        "C#",
        "Node.js",
        "FastAPI",
        "Django",
        "Spring Boot",
        "REST APIs",
        "GraphQL",
        "SQL",
        "PostgreSQL",
        "MySQL",
        "MongoDB",
        "Git",
        "Docker",
    ],

    "frontend-development": [
        "HTML",
        "CSS",
        "JavaScript",
        "TypeScript",
        "React",
        "Angular",
        "Vue.js",
        "REST APIs",
        "Git",
        "UI/UX Principles",
        "Responsive Design",
    ],

    "full-stack-development": [
        "HTML",
        "CSS",
        "JavaScript",
        "TypeScript",
        "React",
        "Node.js",
        "Python",
        "Django",
        "FastAPI",
        "REST APIs",
        "SQL",
        "PostgreSQL",
        "MongoDB",
        "Git",
        "Docker",
    ],

    # Data
    "data-science": [
        "Python",
        "Pandas",
        "NumPy",
        "Matplotlib",
        "SQL",
        "Statistics",
        "Data Analysis",
        "Machine Learning",
        "Scikit-learn",
        "TensorFlow",
        "Data Visualization",
    ],

    "artificial-intelligence": [
        "Python",
        "Statistics",
        "Linear Algebra",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "PyTorch",
        "Natural Language Processing",
        "Computer Vision",
        "Generative AI",
        "Large Language Models",
    ],

    "data-engineering": [
        "Python",
        "SQL",
        "PostgreSQL",
        "ETL",
        "Data Pipelines",
        "Apache Spark",
        "Apache Kafka",
        "Data Warehousing",
        "Cloud Computing",
        "Docker",
        "Git",
    ],

    # Cybersecurity
    "cybersecurity": [
        "Networking",
        "TCP/IP",
        "Linux",
        "Windows Security",
        "Python",
        "Network Security",
        "Firewalls",
        "Encryption",
        "Identity and Access Management",
        "Vulnerability Assessment",
        "Penetration Testing",
        "Security Monitoring",
        "SIEM",
        "Incident Response",
    ],

    # Cloud / DevOps
    "cloud-computing": [
        "Cloud Computing",
        "AWS",
        "Microsoft Azure",
        "Google Cloud",
        "Linux",
        "Networking",
        "Virtualization",
        "Docker",
        "Kubernetes",
        "Terraform",
        "Infrastructure as Code",
        "Cloud Security",
    ],

    "devops": [
        "Linux",
        "Git",
        "GitHub",
        "CI/CD",
        "Docker",
        "Kubernetes",
        "Jenkins",
        "GitHub Actions",
        "Terraform",
        "AWS",
        "Azure",
        "Monitoring",
        "Infrastructure as Code",
    ],

    # Networking
    "networking": [
        "Networking Fundamentals",
        "TCP/IP",
        "DNS",
        "DHCP",
        "Routing",
        "Switching",
        "LAN",
        "WAN",
        "VPN",
        "Firewalls",
        "Cisco",
        "Network Security",
        "Linux",
    ],

    "systems-administration": [
        "Windows Server",
        "Linux",
        "Active Directory",
        "PowerShell",
        "Bash",
        "Networking",
        "DNS",
        "DHCP",
        "Virtualization",
        "Backup and Recovery",
        "System Monitoring",
        "Cybersecurity",
    ],

    # Databases
    "database-administration": [
        "SQL",
        "PostgreSQL",
        "MySQL",
        "Microsoft SQL Server",
        "Oracle Database",
        "Database Design",
        "Database Security",
        "Backup and Recovery",
        "Performance Tuning",
        "Database Administration",
    ],

    # Testing
    "software-testing": [
        "Software Testing",
        "Test Planning",
        "Test Cases",
        "Manual Testing",
        "API Testing",
        "Postman",
        "Selenium",
        "Playwright",
        "Automation Testing",
        "Performance Testing",
        "Regression Testing",
        "Git",
        "CI/CD",
    ],

    # Analysis
    "business-analysis": [
        "Requirements Gathering",
        "Requirements Analysis",
        "Business Process Modelling",
        "User Stories",
        "Use Cases",
        "UML",
        "Stakeholder Management",
        "Agile",
        "Scrum",
        "Jira",
        "Confluence",
        "SQL",
    ],

    "systems-analysis": [
        "Systems Analysis",
        "Requirements Engineering",
        "UML",
        "System Design",
        "Database Design",
        "SQL",
        "API Design",
        "Software Development Life Cycle",
        "Agile",
        "Scrum",
        "Documentation",
    ],

    # Management
    "it-project-management": [
        "Project Management",
        "Agile",
        "Scrum",
        "Kanban",
        "Project Planning",
        "Risk Management",
        "Stakeholder Management",
        "Jira",
        "Confluence",
        "Microsoft Project",
        "IT Governance",
    ],

    # IT Support
    "it-support": [
        "Hardware Troubleshooting",
        "Software Troubleshooting",
        "Windows",
        "Linux",
        "Networking",
        "TCP/IP",
        "Active Directory",
        "Microsoft 365",
        "Technical Support",
        "IT Service Management",
        "Jira Service Management",
        "Ticket Management",
    ],

    "it-service-management": [
        "IT Service Management",
        "ITIL",
        "Incident Management",
        "Problem Management",
        "Change Management",
        "Service Requests",
        "Service Level Management",
        "Jira Service Management",
        "Confluence",
        "Service Desk",
    ],

    # Design
    "ui-ux-design": [
        "UI Design",
        "UX Design",
        "Figma",
        "Wireframing",
        "Prototyping",
        "User Research",
        "Usability Testing",
        "Information Architecture",
        "Responsive Design",
        "Design Systems",
    ],

    # Emerging Technologies
    "blockchain": [
        "Blockchain",
        "Cryptography",
        "Distributed Systems",
        "Smart Contracts",
        "Solidity",
        "Ethereum",
        "Web3",
        "JavaScript",
        "Python",
        "Cybersecurity",
    ],

    "iot": [
        "Internet of Things",
        "Python",
        "C",
        "C++",
        "Embedded Systems",
        "Microcontrollers",
        "Sensors",
        "MQTT",
        "Networking",
        "Cloud Computing",
        "Data Analytics",
    ],
}


def analyze_against_roadmap(
    cv_skills: List[str],
    roadmap: str
) -> Dict:

    roadmap_key = roadmap.strip().lower()

    if roadmap_key not in ROADMAP_SKILLS:
        raise ValueError(
            f"Invalid roadmap: {roadmap}. "
            f"Available roadmaps: {', '.join(ROADMAP_SKILLS.keys())}"
        )

    roadmap_skills = ROADMAP_SKILLS[roadmap_key]

    cv_skill_lookup = {
        skill.strip().lower()
        for skill in cv_skills
        if skill and skill.strip()
    }

    missing_skills = [
        skill
        for skill in roadmap_skills
        if skill.lower() not in cv_skill_lookup
    ]

    matched_skills = [
        skill
        for skill in roadmap_skills
        if skill.lower() in cv_skill_lookup
    ]

    total_skills = len(roadmap_skills)
    matched_count = len(matched_skills)

    match_percentage = round(
        (matched_count / total_skills) * 100,
        2
    ) if total_skills else 0

    if len(missing_skills) > 6:
        priority_level = "High"
    elif len(missing_skills) > 0:
        priority_level = "Medium"
    else:
        priority_level = "None"

    return {
        "roadmap": roadmap_key,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_percentage": match_percentage,
        "recommended_learning": [
            f"Learn or practice: {skill}"
            for skill in missing_skills
        ],
        "priority_level": priority_level,
    }