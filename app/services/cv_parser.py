
import io
import re

import pdfplumber
import docx


def extract_text(file_bytes: bytes, extension: str) -> str:
    if extension == "pdf":
        return _extract_pdf_text(file_bytes)
    elif extension == "docx":
        return _extract_docx_text(file_bytes)
    else:
        raise ValueError(f"Unsupported extension: {extension}")


def _extract_pdf_text(file_bytes: bytes) -> str:
    text_parts = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)

        # If no selectable text was found, attempt an optional OCR fallback
        if not text_parts:
            try:
                from PIL import Image
                import pytesseract

                for page in pdf.pages:
                    try:
                        pil_image = page.to_image(resolution=300).original
                        ocr_text = pytesseract.image_to_string(pil_image)
                        if ocr_text and ocr_text.strip():
                            text_parts.append(ocr_text)
                    except Exception:
                        # If a single page fails OCR, continue with others
                        continue
            except Exception:
                # pytesseract or PIL not installed / available — skip OCR
                pass

    return "\n".join(text_parts)


def _extract_docx_text(file_bytes: bytes) -> str:
    document = docx.Document(io.BytesIO(file_bytes))

    return "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    )


EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

PHONE_PATTERN = re.compile(r"(\+?\d[\d\s().-]{7,}\d)")

# Starter keyword list — expand this as you build out skills-gap analysis
SKILL_KEYWORDS = [
    "python", "java", "javascript", "typescript", "sql", "fastapi",
    "django", "flask", "react", "node.js", "postgresql", "mongodb",
    "docker", "kubernetes", "aws", "azure", "gcp", "git", "linux",
    "c++", "c#", "html", "css", "rest api", "graphql", "ci/cd",
]

SECTION_HEADERS = ["experience", "education", "skills", "projects", "certifications"]


def parse_cv(text: str) -> dict:
    lower_text = text.lower()

    email_match = EMAIL_PATTERN.search(text)
    phone_match = PHONE_PATTERN.search(text)

    found_skills = [
        skill for skill in SKILL_KEYWORDS
        if skill in lower_text
    ]

    sections = _split_sections(text)

    return {
        "email": email_match.group(0) if email_match else None,
        "phone": phone_match.group(0).strip() if phone_match else None,
        "skills": found_skills,
        "sections": sections,
        "word_count": len(text.split()),
    }


def _split_sections(text: str) -> dict:
    """Section splitter: treats short, header-like lines containing a known
    keyword as section breaks, rather than requiring the line to start with it."""
    lines = text.split("\n")
    sections: dict[str, list[str]] = {}
    current_section = "summary"
    sections[current_section] = []

    for line in lines:
        stripped = line.strip()
        matched_header = _match_header(stripped)

        if matched_header:
            current_section = matched_header
            sections.setdefault(current_section, [])
        else:
            sections[current_section].append(line)

    return {
        section: "\n".join(content).strip()
        for section, content in sections.items()
        if "\n".join(content).strip()
    }


def _match_header(line: str) -> str | None:
    # Header lines are short — real body text won't accidentally match this filter
    if not line or len(line) > 40 or len(line.split()) > 5:
        return None

    lower_line = line.lower()

    # Check longer/more specific headers first so "work experience" wins over "experience"
    for header in sorted(SECTION_HEADERS, key=len, reverse=True):
        if header in lower_line:
            # Normalize "work experience" -> "experience", "technical skills" -> "skills", etc.
            if "experience" in header:
                return "experience"
            if "skills" in header:
                return "skills"
            if "summary" in header:
                return "summary"
            return header

    return None