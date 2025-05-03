import streamlit as st
import sqlite3
import pandas as pd
from datetime import date
from utils.resume_parser import parse_resume
from utils.jd_parser import extract_skills_from_jd
from utils.skill_matcher import compare_skills

# --- DB Connection ---
def get_connection():
    return sqlite3.connect("tracker.db", check_same_thread=False)

conn = get_connection()
cursor = conn.cursor()

# --- UI Layout ---
st.set_page_config(page_title="Job Tracker", layout="centered")
st.title("📌 Resume / Job Tracker with AI Insights")

menu = st.sidebar.radio("Go to", ["Add Job", "View Applications"])
if st.sidebar.button("Test Resume Parser"):
    from utils.resume_parser import parse_resume
    resume_skills = parse_resume("your_resume.pdf")  # make sure this file exists
    st.write("🧠 Extracted Skills from Resume:", resume_skills)

if st.sidebar.button("Test JD Parser"):
    sample_jd = """
    We are looking for a Data Engineer with experience in Python, SQL, Snowflake, and Airflow.
    Familiarity with Azure and Power BI is a plus. Strong communication skills required.
    """
    jd_skills = extract_skills_from_jd(sample_jd)
    st.write("🧾 Extracted Skills from Job Description:", jd_skills)

if st.sidebar.button("Test Skill Match"):
    from utils.resume_parser import parse_resume
    from utils.jd_parser import extract_skills_from_jd

    resume_skills = parse_resume("your_resume.pdf")
    jd_text = """
    We are hiring a Data Analyst with experience in SQL, Python, Tableau, and Power BI.
    Knowledge of Excel and Azure is an advantage.
    """
    jd_skills = extract_skills_from_jd(jd_text)

    result = compare_skills(resume_skills, jd_skills)

    st.write(f"🧠 **Match %**: {result['match_percent']}%")
    st.write("✅ **Matched Skills**:", result["matched_skills"])
    st.write("❌ **Missing Skills**:", result["missing_skills"])

# --- Add Job Form ---
if menu == "Add Job":
    st.subheader("📝 Add New Job Application")

    with st.form("job_form"):
        company = st.text_input("Company Name")
        role = st.text_input("Job Role")
        status = st.selectbox("Application Status", ["Applied", "Interviewing", "Rejected", "Offer"])
        job_desc = st.text_area("Paste Job Description Here")
        applied_on = st.date_input("Date Applied", value=date.today())

        submitted = st.form_submit_button("Save")
        if submitted:
            cursor.execute("""
                INSERT INTO jobs (company, role, status, job_desc, applied_on)
                VALUES (?, ?, ?, ?, ?)
            """, (company, role, status, job_desc, applied_on))
            conn.commit()
            st.success("✅ Job application saved!")

# --- View Applications ---
elif menu == "View Applications":
    st.subheader("📋 All Saved Applications")
    df = pd.read_sql_query("SELECT * FROM jobs ORDER BY applied_on DESC", conn)
    st.dataframe(df)
