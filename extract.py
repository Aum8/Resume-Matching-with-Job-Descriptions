from pdfminer.high_level import extract_text
import re

def extract_text_from_pdf(pdf_path):
    text = extract_text(pdf_path)
    # pdf_reader = PdfReader(pdf_path)
    # for page in pdf_reader.pages:
    #     text += page.extract_text()
    return text

def extract_resume_details(text):
    # Define patterns
    education_pattern = r"Education\n(.+)"
    skills_pattern = r"Skills\n\n?(.+)"

    # Extract details
    education_match = re.search(education_pattern, text)
    skills_match = re.search(skills_pattern, text)

    education = education_match.group(1) if education_match else "N/A"
    skills = skills_match.group(1) if skills_match else "N/A"

    return {
        "Skills": skills.strip(),
        "Education": education.strip(),
    }


if __name__ == "__main__":
    pdf_path = "archive (1)/data/data/BUSINESS-DEVELOPMENT/11289482.pdf"

    # Extract text from PDF
    resume_text = extract_text_from_pdf(pdf_path)
    with open("resume_text.txt", "w", encoding="utf-8") as text_file:
        text_file.write(resume_text)

    details = extract_resume_details(resume_text)

    print("Skills:", details["Skills"])
    print("Education:", details["Education"])