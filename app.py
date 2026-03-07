import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from pdf_ingestion import (extract_text_from_pdf)
from skill_extraction import (extract_skills)

def initialize():
    st.set_page_config(
        page_title=" >> Hire Honker <<",
        page_icon="🪿",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title(">> Hire Honker <<")

    if "resume_saved" not in st.session_state:
        st.session_state["resume_saved"] = False

    if "resume_skills" not in st.session_state:
        st.session_state["resume_skills"] = None

    if "job_analyzed" not in st.session_state:
        st.session_state["job_analyzed"] = False

    if "job_skills" not in st.session_state:
        st.session_state["job_skills"] = None

def sidebar_uploads():
    with st.sidebar:
        st.markdown("Upload your files here:")

        # Should only be uploaded once
        uploaded_resume = st.file_uploader("Upload your Resume", type="pdf")

        if st.button("Save Resume"):
            if uploaded_resume:
                with st.spinner("Saving..."):
                    resume_text = extract_text_from_pdf(uploaded_resume)
                    all_skills = extract_skills(resume_text)
                    st.session_state["resume_skills"] = all_skills
                    st.session_state["resume_saved"] = True
            else:
                st.warning("You need to upload a resume first")

        if st.session_state["resume_saved"]:
            st.success("Resume saved!")

        # Should have to be changed every time
        uploaded_job_desc = st.file_uploader("Upload the job description", type="pdf")

        analyze_job = st.button("Analyze Job")

        # This is a button that exists in the sidebar but will also trigger something on the main page!
        if analyze_job:
            if uploaded_job_desc:
                with st.spinner("Analyzing..."):
                    saved_job_desc = uploaded_job_desc
                    st.session_state["job_analyzed"] = True

            else:
                st.warning("You need to upload your job description first")

        if st.session_state["job_analyzed"]:
            st.success("Job description analyzed!")

def render_dashboard():
    with st.expander("Resume vs. Dataset Analytics", expanded=False):
        if st.session_state["resume_skills"] is not None:
            # Top section — resume health against dataset
            pass
        else:
            st.info("Upload and save your resume to see analytics here.")

    with st.expander("Resume vs. Job Description Analytics", expanded=False):
        if st.session_state["job_analyzed"]:
            # Bottom section — job match
            pass
        else:
            st.info("Upload and analyze a job description to see results here.")

def main():
    initialize()
    sidebar_uploads()
    render_dashboard()

if __name__ == "__main__":
    main()