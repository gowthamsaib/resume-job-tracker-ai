import re
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_skills_from_jd(jd_text: str) -> list:
    jd_text = jd_text.lower()
    doc = nlp(jd_text)

    # Extract noun chunks (phrases like "data engineering", "python development")
    keywords = set(chunk.text.strip() for chunk in doc.noun_chunks if len(chunk.text.strip()) > 2)

    # Optionally, clean up short/stop words and filter
    filtered_skills = [
        kw for kw in keywords
        if len(kw) >= 3 and not kw.lower() in nlp.Defaults.stop_words
    ]

    return sorted(set(filtered_skills))