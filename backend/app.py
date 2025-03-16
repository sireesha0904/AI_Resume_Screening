from flask import Flask, request, jsonify
from flask_cors import CORS
import docx
import PyPDF2
import re

app = Flask(__name__)
CORS(app)

# Predefined skill set for scoring (expand as needed)
SKILL_KEYWORDS = {"python", "sql", "excel", "machine learning", "data analysis", "java", "aws", "flask"}

def extract_resume_text(file):
    """Extracts text from uploaded PDF or DOCX resume."""
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
    """Attempts to extract the candidate's name (first capitalized phrase)."""
    name_match = re.findall(r"\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)+\b", resume_text)
    return name_match[0] if name_match else "Unknown"

def extract_qualifications(resume_text):
    """Extracts skills from the resume by matching predefined keywords."""
    found_skills = {skill.lower() for skill in SKILL_KEYWORDS if skill.lower() in resume_text.lower()}
    return list(found_skills) if found_skills else ["No skills detected"]

def calculate_resume_score(found_skills):
    """Calculates a resume match score based on extracted skills."""
    if not found_skills or found_skills == ["No skills detected"]:
        return "0%"
    score = (len(found_skills) / len(SKILL_KEYWORDS)) * 100
    return f"{round(score, 2)}%"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        
        file = request.files['resume']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        resume_text = extract_resume_text(file)

        if not resume_text:
            return jsonify({'error': 'Failed to extract text. Try another file.'}), 400

        candidate_name = extract_name(resume_text)
        extracted_skills = extract_qualifications(resume_text)
        resume_score = calculate_resume_score(extracted_skills)

        # Prepare response
        result = {
            "name": candidate_name,
            "qualifications": extracted_skills,
            "resume_score": resume_score,
            "resume_preview": resume_text[:500]  # Show first 500 characters
        }

        return jsonify(result)

    except Exception as e:
        print("Error while processing resume:", e)
        return jsonify({'error': 'An error occurred while processing the resume'}), 500

if __name__ == '__main__':
    app.run(debug=True)
