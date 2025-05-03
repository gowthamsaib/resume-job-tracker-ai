import pdfplumber
import re

# Optional: you can maintain a list of known skills to match against
KNOWN_SKILLS = [
    "python", "sql", "tableau", "power bi", "excel", "snowflake",
    "azure", "aws", "pandas", "numpy", "spark", "hadoop", "etl", "airflow",
    "data engineering", "data analysis", "machine learning", "nlp", "scikit-learn",
    "git", "jira", "confluence", "data visualization", "data wrangling"
]

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.lower()

def extract_skills_from_text(text: str) -> list:
    found_skills = []
    for skill in KNOWN_SKILLS:
        if re.search(rf"\b{re.escape(skill)}\b", text):
            found_skills.append(skill)
    return sorted(set(found_skills))

def parse_resume(file_path: str) -> list:
    raw_text = extract_text_from_pdf(file_path)
    return extract_skills_from_text(raw_text)