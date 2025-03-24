from flask import Flask, request, jsonify
from flask_cors import CORS
import docx
import PyPDF2
import re

app = Flask(__name__)
CORS(app)

# Predefined skill set with common technologies (add more if needed)
SKILL_KEYWORDS = {
    "python", "sql", "excel", "machine learning", "data analysis", "java",
    "aws", "flask", "html", "css", "javascript", "angular", "spring boot", "git"
}

def extract_resume_text(file):
    """Extract text from PDF or DOCX resume."""
    resume_text = ""

    if file.filename.lower().endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text + "\n"

    elif file.filename.lower().endswith('.docx'):
        doc = docx.Document(file)
        resume_text = '\n'.join([para.text for para in doc.paragraphs])

    return resume_text.strip()

def extract_name(resume_text):
    """Extract candidate name by checking common formats."""
    lines = resume_text.strip().split('\n')[:10]  # Only look at first 10 lines
    for line in lines:
        line = line.strip()
        # Check if line is all uppercase and looks like a name
        if line.isupper() and 3 < len(line) < 40 and ' ' in line:
            return line.title()
        # If line starts with Name:
        if re.match(r'(Name|NAME)[:\-]\s*(.+)', line):
            return re.match(r'(Name|NAME)[:\-]\s*(.+)', line).group(2).strip().title()

    # Fallback: first two capitalized words in the first 10 lines
    name_match = re.findall(r"\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)+\b", "\n".join(lines))
    return name_match[0] if name_match else "Unknown"

def extract_qualifications(resume_text):
    """Extract skills from resume text with proper word boundaries."""
    found_skills = set()
    lower_resume = resume_text.lower()
    for skill in SKILL_KEYWORDS:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, lower_resume, re.IGNORECASE):
            found_skills.add(skill.lower())
    return list(found_skills) if found_skills else ["No skills detected"]

def calculate_resume_score(found_skills):
    """Calculate resume score."""
    if not found_skills or found_skills == ["No skills detected"]:
        return "0%"
    score = (len(found_skills) / len(SKILL_KEYWORDS)) * 100
    return f"{round(score, 2)}%"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file part in the request'}), 400

        file = request.files['resume']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        resume_text = extract_resume_text(file)

        if not resume_text:
            return jsonify({'error': 'Failed to extract text. Try another file.'}), 400

        candidate_name = extract_name(resume_text)
        extracted_skills = extract_qualifications(resume_text)
        resume_score = calculate_resume_score(extracted_skills)

        # Handle job description if provided or set default
        job_description = request.form.get('job_description', 'Not provided')
        if job_description == 'undefined' or not job_description.strip():
            job_description = 'Not provided'

        # Prepare final response
        result = {
            "job_description": job_description,
            "name": candidate_name,
            "qualifications": extracted_skills,
            "resume_score": resume_score,
            "resume_preview": resume_text[:500]  # First 500 characters preview
        }

        return jsonify(result)

    except Exception as e:
        print("Error while processing resume:", e)
        return jsonify({'error': 'An error occurred while processing the resume'}), 500

if __name__ == '__main__':
    app.run(debug=True)
