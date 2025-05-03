def compare_skills(resume_skills: list, jd_skills: list) -> dict:
    resume_set = set([s.lower() for s in resume_skills])
    jd_set = set([s.lower() for s in jd_skills])

    matched_skills = sorted(resume_set & jd_set)
    missing_skills = sorted(jd_set - resume_set)

    if len(jd_set) == 0:
        match_percent = 0
    else:
        match_percent = round((len(matched_skills) / len(jd_set)) * 100, 2)

    return {
        "match_percent": match_percent,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }