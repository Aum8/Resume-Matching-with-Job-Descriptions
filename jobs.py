from datasets import load_dataset
import json

dataset = load_dataset("jacob-hugging-face/job-descriptions")

# Extract job descriptions
num_descriptions = 15
job_descriptions = dataset['train']['job_description'][:num_descriptions]
position_titles = dataset['train']['position_title'][:num_descriptions]
C = dataset['train']['model_response'][:num_descriptions]

# Save the job descriptions to a text file
with open("job_text.txt", "w", encoding="utf-8") as text_file:
    for idx, (description, cat, res) in enumerate(zip(job_descriptions, position_titles, C), start=1):
        text_file.write(f"Job Description {idx}:\n{description}\n\n")
        text_file.write(f"Job category {idx}:\n{cat}\n\n")
        
        # Check if 'res' is a valid JSON string
        try:
            res_json = json.loads(res)
            required_skills = res_json.get('Required Skills', '')
            if required_skills.strip() == '{}' or required_skills.strip() == '':
                text_file.write(f"Required Skills {idx}:\nNo specific skills listed\n\n")
            else:
                required_skills_formatted = json.dumps(required_skills, indent=2)
                text_file.write(f"Required Skills {idx}:\n{required_skills_formatted}\n\n")
        except json.JSONDecodeError:
            text_file.write(f"Required Skills {idx}:\n{res}\n\n")
