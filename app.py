import streamlit as st

st.set_page_config(page_title="Job Tracker", layout="centered")
st.title("📌 Resume / Job Tracker with AI Insights")

st.sidebar.title("🔍 Navigation")
menu = st.sidebar.radio("Go to", ["Home", "Add Job", "View Applications"])

st.markdown("👋 Welcome! Start by adding job descriptions and compare them with your resume.")
