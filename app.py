import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from pdf_ingestion import extract_text_from_pdf
from skill_extraction import extract_skills, ROLES
from resume_matcher import calculate_resume_match
from analyze_job_skills import get_final_market_analysis
from RIS_Calculator import RIS_calculator

def initialize():
    st.set_page_config(
        page_title="Hire Honker",
        page_icon="🪿",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Space+Grotesk:wght@500;700&family=DM+Mono:wght@400;500&display=swap');

    :root {
        --bg:         #0f0f0f;
        --surface:    #1a1a1a;
        --surface2:   #222222;
        --border:     #2e2e2e;
        --accent:     #f0a500;
        --accent-dim: #7a5200;
        --text:       #f0ede8;
        --muted:      #6b6b6b;
    }

    /* ── Global ── */
    html, body, .stApp {
        background-color: var(--bg) !important;
        color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* ── Hide Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 2rem 3rem 4rem !important; max-width: 1200px; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: var(--surface) !important;
        border-right: 1px solid var(--border) !important;
    }
    [data-testid="stSidebar"] * { color: var(--text) !important; }

    /* ── Buttons ── */
    .stButton > button {
        background: transparent !important;
        border: 1px solid var(--accent) !important;
        color: var(--accent) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        border-radius: 3px !important;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background: var(--accent) !important;
        color: var(--bg) !important;
    }

    /* ── Expanders ── */
    .stExpander {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 6px !important;
        margin-bottom: 1rem !important;
    }
    .stExpander summary {
        background: var(--surface2) !important;
    }

    /* ── Alerts ── */
    .stAlert {
        background: var(--surface2) !important;
        border-left: 3px solid var(--accent) !important;
        color: var(--text) !important;
        border-radius: 4px !important;
    }

    /* ── File uploader ── */
    [data-testid="stFileUploader"] {
        background: var(--surface2) !important;
        border: 1px dashed var(--border) !important;
        border-radius: 4px !important;
    }

    /* ── Headings ── */
    h1 {
        font-size: 4.0rem;
        color: var(--accent);
        font-family: 'DM Mono', monospace;
    }
    </style>

    <h1>🪿 Hire Honker</h1>

    <div style="
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        color: #6b6b6b;
        margin-bottom: 2rem;
    ">Resume Intelligence Platform</div>
    """, unsafe_allow_html=True)

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
        st.image("HireHonker.png", width=350)
        st.markdown("Upload your files here:")

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

        st.selectbox(
            "Filter by job type",
            options=["All"] + ROLES,
            key="selected_role"
        )

        uploaded_job_desc = st.file_uploader("Upload the job description", type="pdf")

        analyze_job = st.button("Analyze Job")

        if analyze_job:
            if uploaded_job_desc and uploaded_resume:
                with st.spinner("Analyzing..."):
                    job_text = extract_text_from_pdf(uploaded_job_desc)
                    job_skills = extract_skills(job_text)
                    st.session_state["job_skills"] = job_skills
                    st.session_state["job_analyzed"] = True

                    resume_skills, matched_skills, missing_skills, match_score = calculate_resume_match(resume_text,job_text)

                    skill_category_lists = get_final_market_analysis(job_skills, threshold=85)
                    final_score = RIS_calculator(matched_skills, missing_skills, skill_category_lists)

            elif uploaded_job_desc and not uploaded_resume:
                st.warning("You need to upload your resume too!")
            else:
                st.warning("You need to upload your job description")

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