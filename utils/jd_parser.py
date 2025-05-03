import re

# Same known skills list — keep in sync with resume_parser
KNOWN_SKILLS = [
    "python", "sql", "tableau", "power bi", "excel", "snowflake",
    "azure", "aws", "pandas", "numpy", "spark", "hadoop", "etl", "airflow",
    "data engineering", "data analysis", "machine learning", "nlp", "scikit-learn",
    "git", "jira", "confluence", "data visualization", "data wrangling"
]

def extract_skills_from_jd(jd_text: str) -> list:
    jd_text = jd_text.lower()
    found_skills = []
    for skill in KNOWN_SKILLS:
        if re.search(rf"\b{re.escape(skill)}\b", jd_text):
            found_skills.append(skill)
    return sorted(set(found_skills))
