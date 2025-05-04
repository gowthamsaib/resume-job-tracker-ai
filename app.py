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

# --- UI Setup ---
st.set_page_config(page_title="Job Tracker", layout="centered")

# --- Page Banner ---
st.markdown("""
    <div style='text-align: center; padding: 1rem 0; background-color: #f0f4f8; border-radius: 10px;'>
        <h1 style='color: #333;'>📌 Resume & Job Tracker with AI Insights</h1>
        <p style='color: #666; font-size: 16px;'>Track your job applications and let AI match your resume with job descriptions.</p>
    </div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio("🔍 Navigate", ["Add Job", "View Applications"])

# --- Add Job Form ---
if menu == "Add Job":
    st.markdown("### 📝 <span style='color:#3366cc'>Add New Job Application</span>", unsafe_allow_html=True)

    with st.form("job_form"):
        company = st.text_input("Company Name")
        role = st.text_input("Job Role")
        status = st.selectbox("Application Status", ["Applied", "Interviewing", "Rejected", "Offer"])
        job_desc = st.text_area("Paste Job Description Here")
        applied_on = st.date_input("Date Applied", value=date.today())
        uploaded_resume = st.file_uploader("Upload Your Resume (PDF)", type="pdf")

        submitted = st.form_submit_button("Save and Analyze")

        if submitted:
            if job_desc.strip() == "":
                st.error("❗ Please paste a job description.")
            else:
                # Save job to DB
                cursor.execute("""
                    INSERT INTO jobs (company, role, status, job_desc, applied_on)
                    VALUES (?, ?, ?, ?, ?)
                """, (company, role, status, job_desc, applied_on))
                conn.commit()
                st.success("✅ Job application saved!")

                # Resume file (uploaded or fallback)
                if uploaded_resume:
                    with open("temp_resume.pdf", "wb") as f:
                        f.write(uploaded_resume.read())
                    resume_path = "temp_resume.pdf"
                else:
                    resume_path = "default_resume.pdf"

                resume_skills = parse_resume(resume_path)
                jd_skills = extract_skills_from_jd(job_desc)
                result = compare_skills(resume_skills, jd_skills)

                st.markdown("---")
                st.markdown("### 🧠 <span style='color:#3366cc'>AI Skill Match Insights</span>", unsafe_allow_html=True)

                st.markdown(f"""
                    <div style='text-align:center; font-weight:bold; font-size:18px; margin-bottom:10px;'>
                        🔎 Match Score: {result['match_percent']}%
                    </div>
                """, unsafe_allow_html=True)
                st.progress(min(result['match_percent'] / 100, 1.0))

                if result["matched_skills"]:
                    st.success(f"✅ Matched Skills: {', '.join(result['matched_skills'])}")
                else:
                    st.info("No matched skills found.")

                if result["missing_skills"]:
                    st.warning(f"❌ Missing Skills: {', '.join(result['missing_skills'])}")
                else:
                    st.success("Perfect match! No missing skills.")

# --- View Applications ---
elif menu == "View Applications":
    st.markdown("### 📋 <span style='color:#3366cc'>All Saved Applications</span>", unsafe_allow_html=True)

    df = pd.read_sql_query("SELECT * FROM jobs ORDER BY applied_on DESC", conn)
    st.dataframe(df)

    if not df.empty:
        job_ids = df["id"].tolist()
        selected_id = st.selectbox("Select Job ID", job_ids)

        selected_job = df[df["id"] == selected_id].iloc[0]
        st.markdown("### 🗂️ <span style='color:#3366cc'>Job Details</span>", unsafe_allow_html=True)

        st.write(f"**Company:** {selected_job['company']}")
        st.write(f"**Role:** {selected_job['role']}")
        st.write(f"**Status:** {selected_job['status']}")
        st.write(f"**Applied On:** {selected_job['applied_on']}")

        st.markdown("**Job Description:**")
        st.markdown(f"""
            <div style='background:#f9f9f9;padding:1em;border-radius:8px;max-height:300px;overflow-y:auto;'>
                {selected_job['job_desc']}
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            show_edit_form = st.button("✏️ Edit Job")
        with col2:
            if st.button("🗑️ Delete Job"):
                cursor.execute("DELETE FROM jobs WHERE id=?", (selected_id,))
                conn.commit()
                st.warning("🗑️ Job deleted!")
                

        if show_edit_form:
            st.markdown("### ✏️ <span style='color:#3366cc'>Update Job Details</span>", unsafe_allow_html=True)
            with st.form("edit_form"):
                new_company = st.text_input("Company Name", value=selected_job["company"])
                new_role = st.text_input("Job Role", value=selected_job["role"])
                new_status = st.selectbox("Status", ["Applied", "Interviewing", "Rejected", "Offer"],
                                          index=["Applied", "Interviewing", "Rejected", "Offer"].index(selected_job["status"]))
                new_job_desc = st.text_area("Job Description", value=selected_job["job_desc"])
                new_applied_on = st.date_input("Applied On", value=pd.to_datetime(selected_job["applied_on"]))

                update = st.form_submit_button("Update Job")
                if update:
                    cursor.execute("""
                        UPDATE jobs
                        SET company=?, role=?, status=?, job_desc=?, applied_on=?
                        WHERE id=?
                    """, (new_company, new_role, new_status, new_job_desc, new_applied_on, selected_id))
                    conn.commit()
                    st.success("✅ Job updated!")
                    