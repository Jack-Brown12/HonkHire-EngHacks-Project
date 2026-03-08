import streamlit as st
import pandas as pd
from pdf_ingestion import extract_text_from_pdf
from skill_extraction import extract_skills
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

    html, body, .stApp {
        background-color: var(--bg) !important;
        color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
    }

    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 2rem 3rem 4rem !important; max-width: 1200px; }

    [data-testid="stSidebar"] {
        background: var(--surface) !important;
        border-right: 1px solid var(--border) !important;
    }
    [data-testid="stSidebar"] * { color: var(--text) !important; }

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

    session_keys = {
        "resume_saved": False,
        "resume_skills": [],
        "job_analyzed": False,
        "job_skills": [],
        "skill_category_lists": {"core_skills": [], "optional_skills": [], "rare_skills": []},
        "final_score": 0
    }

    for key, value in session_keys.items():
        if key not in st.session_state:
            st.session_state[key] = value

def sidebar_uploads():
    with st.sidebar:
        st.image("HireHonker.png", width=350)
        st.markdown("### Upload Documents")
        uploaded_resume = st.file_uploader("Upload Resume", type="pdf")
        uploaded_job_desc = st.file_uploader("Upload Job Description", type="pdf")

        if st.button("Analyze Job"):
            if uploaded_resume and uploaded_job_desc:
                with st.spinner("Analyzing..."):
                    resume_text = extract_text_from_pdf(uploaded_resume)
                    res_skills = extract_skills(resume_text)
                    st.session_state["resume_skills"] = res_skills
                    st.session_state["resume_saved"] = True

                    job_text = extract_text_from_pdf(uploaded_job_desc)
                    job_skills = extract_skills(job_text)
                    st.session_state["job_skills"] = job_skills

                    categories = get_final_market_analysis(job_skills, threshold=85)
                    st.session_state["skill_category_lists"] = categories

                    score = RIS_calculator(res_skills, categories)
                    st.session_state["final_score"] = score
                    st.session_state["job_analyzed"] = True
            else:
                st.warning("Please upload both documents to continue.")

def render_dashboard():
    if st.session_state["job_analyzed"]:
        score = st.session_state["final_score"]
        market = st.session_state["skill_category_lists"]
        res_skills = {s.lower() for s in st.session_state["resume_skills"]}

        st.divider()
        st.markdown("## Analysis Results")
        
        col1, col2 = st.columns(2)
        col1.metric("Realistic Application Score", f"{score}%")
        core_match_count = len([s for s in market["core_skills"] if s.lower() in res_skills])
        col2.metric("Core Skills Found", core_match_count)

        st.markdown("---")
        
        tab1, tab2, tab3 = st.tabs(["Skill Breakdown", "Resume Inventory", "Final Assessment"])

        with tab1:
            c1, c2, c3 = st.columns(3)
            def sort_matched(s_list):
                return sorted(s_list, key=lambda x: x.lower() in res_skills, reverse=True)

            with c1:
                st.markdown("### Common (Core)")
                for s in sort_matched(market["core_skills"]):
                    if s.lower() in res_skills: st.success(f"Matched: {s}")
                    else: st.error(f"Missing: {s}")
            
            with c2:
                st.markdown("### Uncommon (Optional)")
                for s in sort_matched(market["optional_skills"]):
                    if s.lower() in res_skills: st.success(f"Matched: {s}")
                    else: st.warning(f"Missing: {s}")

            with c3:
                st.markdown("### Rare")
                for s in sort_matched(market["rare_skills"]):
                    if s.lower() in res_skills: st.info(f"Bonus: {s}")
                    else: st.write(f"Optional: {s}")

        with tab2:
            st.markdown("### All Skills Detected on Your Resume")
            user_skills = st.session_state["resume_skills"]
            if user_skills:
                res_col1, res_col2 = st.columns(2)
                mid = (len(user_skills) + 1) // 2
                with res_col1:
                    for s in user_skills[:mid]: st.success(s)
                with res_col2:
                    for s in user_skills[mid:]: st.success(s)
            else:
                st.write("No skills detected.")

        with tab3:
            st.markdown("### Final Suitability Report")
            if score >= 70:
                st.success(f"### Score: {score}% - Excellent Match")
                st.write("You have a strong command of the core requirements. You are highly competitive for this role.")
            elif 40 <= score < 70:
                st.warning(f"### Score: {score}% - Solid Potential")
                st.write("You match many requirements, but core gaps exist. Consider focusing on the missing core skills listed in the breakdown.")
            else:
                st.error(f"### Score: {score}% - Stretch Goal")
                st.write("This score is below the market average for this role. This description may be inflated. Apply anyway and focus on your ability to learn quickly.")
            
            st.info("The Realistic Application Score ignores rare skills that are often part of requirement inflation. Missing them does not lower your score.")

    else:
        st.info("Upload your Resume and Job Description in the sidebar to begin.")

def main():
    initialize()
    sidebar_uploads()
    render_dashboard()

if __name__ == "__main__":
    main()