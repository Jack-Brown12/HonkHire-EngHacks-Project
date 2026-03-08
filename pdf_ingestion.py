import pdfplumber

def extract_text_from_pdf(file_object) -> str:
    text = ""
    with pdfplumber.open(file_object) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
            
    return text