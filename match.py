import os
from pdfminer.high_level import extract_text
import re
import json

# Define patterns
education_pattern = r"Education\n(.+)"
skills_pattern = r"Skills\n\n?(.+)"

def extract_text_from_pdf(pdf_path):
    text = extract_text(pdf_path)
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


# Load the job descriptions from the text file
job_descriptions = []
job_categories = []
required_skills_list = []

with open("job_text.txt", "r", encoding="utf-8") as text_file:
    lines = text_file.read().split("\n\n")
    for i in range(0, len(lines), 3):
        job_descriptions.append(lines[i])
        job_categories.append(lines[i + 1])
        if i + 2 < len(lines):  # Check if there's an available line for required skills
            required_skills_text = lines[i + 2]
            if required_skills_text.startswith("Required Skills"):
                try:
                    required_skills_json = json.loads(required_skills_text.split(":\n", 1)[1])
                    required_skills_list.append(required_skills_json)
                except json.JSONDecodeError:
                    required_skills_list.append({})
            else:
                required_skills_list.append({})
        else:
            required_skills_list.append({})

def calculate_matching_score(job, resume):
    job_skills = set(job.get("Required Skills", {}).keys()) if isinstance(job.get("Required Skills"), dict) else set()
    
    # Check if 'Education' key exists in the resume dictionary
    if "Education" in resume:
        resume_education = resume["Education"]
    else:
        resume_education = "N/A"

    # Calculate the Jaccard similarity between job skills and resume skills
    resume_skills = set(resume["Skills"].split(", "))
    skill_similarity = len(job_skills.intersection(resume_skills)) / len(job_skills.union(resume_skills))

    # Education matching score (exact match if 'Education' is not "N/A")
    education_match = 1 if resume_education != "N/A" and job["Education"].lower() == resume_education.lower() else 0

    # Overall matching score (you can adjust the weights as needed)
    overall_score = 0.7 * skill_similarity + 0.3 * education_match

    return overall_score
def calculate_matching_score(job, resume):
    job_skills = set(job.get("Required Skills", {}).keys()) if isinstance(job.get("Required Skills"), dict) else set()
    
    # Check if 'Education' key exists in the resume dictionary
    resume_education = resume.get("Education", "N/A")

    # Calculate the Jaccard similarity between job skills and resume skills
    resume_skills = set(resume["Skills"].split(", "))
    skill_similarity = len(job_skills.intersection(resume_skills)) / len(job_skills.union(resume_skills))

    # Education matching score (exact match if 'Education' is not "N/A")
    if "Education" in job:
        education_match = 1 if resume_education != "N/A" and job["Education"].lower() == resume_education.lower() else 0
    else:
        education_match = 0  # No education requirement, so no match score

    # Overall matching score (you can adjust the weights as needed)
    overall_score = 0.7 * skill_similarity + 0.3 * education_match

    return overall_score



# Create a dictionary to store candidate details
all_candidates = {}

# Iterate through all resume PDFs in a folder
resume_folder = "archive (1)/data/data/BUSINESS-DEVELOPMENT/"  # Replace with the path to your resume folder
for filename in os.listdir(resume_folder):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(resume_folder, filename)

        # Extract text from the resume PDF
        resume_text = extract_text_from_pdf(pdf_path)
        resume_details = extract_resume_details(resume_text)

        # Store resume details in the dictionary
        all_candidates[filename] = resume_details

# Create a dictionary to store top candidates for each job
top_candidates = {}

# Match candidates for each job
for i, job_description in enumerate(job_descriptions):
    job = {
        "Description": job_description,
        "Category": job_categories[i],
        "Required Skills": required_skills_list[i],
    }

    # Calculate scores for all candidates (resumes)
    candidate_scores = []
    for candidate_name, candidate_details in all_candidates.items():
        score = calculate_matching_score(job, candidate_details)
        candidate_scores.append((score, candidate_name))

    # Sort candidates by score (highest to lowest)
    candidate_scores.sort(reverse=True, key=lambda x: x[0])

    # Select the top 5 candidates for each job
    top_candidates[job["Category"]] = candidate_scores[:5]

# Print the top 5 candidates for each job
for category, candidates in top_candidates.items():
    print(f"Top 5 Candidates for {category} Jobs:")
    for i, (score, candidate_name) in enumerate(candidates, start=1):
        print(f"  Candidate {i} - Matching Score: {score:.2f}")
        print(f"    Candidate Name: {candidate_name}")
        print(f"    Skills: {all_candidates[candidate_name]['Skills']}")
        print(f"    Education: {all_candidates[candidate_name]['Education']}")
    print()
