import pdfplumber
from skill_extraction import extract_skills, detect_role
from pdf_ingestion import extract_text_from_pdf


pdf_file = "/Users/jacksmacbook/Desktop/Software Developer (Co-op) - AI Adoption-460539.pdf"



def main():
    text = extract_text_from_pdf(pdf_file)
    # 2. Extract skills
    skills = extract_skills(text)

    print(text)

    # 3. Detect role
    role = detect_role(text)

    # 4. Print results
    print("---- Job Posting Analysis ----")
    print("Detected Skills:")
    for skill in skills:
        print(skill)

if __name__ == "__main__":
   main()



   #WE NEED: job text resume text, job skills-->market analysis + user resume skills-->final analysis