Database used for job comparison data:
https://www.kaggle.com/datasets/ravindrasinghrana/job-description-dataset

AI used for resume evaluation and comparison:


# Honk Hire 🪿
### Resume Intelligence Plaform for Waterloo Engineering Students

## Overview
Honk Hire helps students understand how well their resume matches a job posting. Users upload a resume PDF and a job posting PDF, and the app extracts skills, compares them, and highlights matched and missing requirements. The goal is to make job applications clearer and easier to evaluate.

## Problem
Engineering students often struggle to tell whether they are actually qualified for a co-op or internship posting. Job descriptions can be unclear, inflated, or overly broad, which makes it hard to know whether to apply. Honk Hire addresses this by turning job postings into structured skill information and comparing them directly with a student's resume.

## Features

- Upload **resume PDF**
- Upload **job posting PDF**
- Extract skills from both documents
- Detect the likely job role from the posting
- Compare resume skills with job requirements
- Generate a **resume–job match score**
- Display:
  - matched skills
  - missing skills
  - competitiveness status
- Market skill analysis using job datasets
- Relevance Index Score (RIS)

## How It Works

1. The user uploads a resume and job posting as PDFs.
2. Text is extracted from both documents.
3. Natural Language Processing identifies skills in the job posting and resume.
4. The system compares the two skill sets.
5. The app calculates a **match score** and **Resume Intelligence Score (RIS)**.
6. Results are displayed in an interactive dashboard.

## Tech Stack

- **Python**
- **Streamlit** – User interface
- **spaCy** – NLP processing
- **RapidFuzz** – skill matching
- **pdfplumber** – PDF text extraction
- **pandas** – data analysis
- **matplotlib** – visual analytics

## Project Structure

```
EngHacks-Project
│
├── app.py                  # Streamlit application
├── pdf_ingestion.py        # PDF text extraction
├── skill_extraction.py     # NLP skill detection
├── resume_matcher.py       # Resume vs job comparison logic
├── analyze_job_skills.py   # Market skill analysis
├── RIS_Calculator.py       # Relevance Index Score
├── requirements.txt
└── README.md

## How to Run

pip install requirements.txt
streamlit run app.py

## Citations

- spaCy — https://spacy.io  
- RapidFuzz — https://github.com/rapidfuzz/RapidFuzz  
- pdfplumber — https://github.com/jsvine/pdfplumber  
- Streamlit — https://streamlit.io  