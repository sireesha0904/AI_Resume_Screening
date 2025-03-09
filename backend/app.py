from flask import Flask, request, jsonify
import os
from utils.text_extractor import extract_text_from_resume
from utils.preprocess import preprocess_text
import pickle
from collections import Counter
import re

app = Flask(__name__)

# Load the trained model
model_path = os.path.join(os.path.dirname(__file__), 'model', 'resume_model.pkl')
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# Function to calculate the qualification score based on skills
def calculate_score(resume_text, skills):
    resume_words = re.findall(r'\w+', resume_text.lower())
    resume_counter = Counter(resume_words)
    matched_skills = [skill for skill in skills if skill in resume_counter]
    score = (len(matched_skills) / len(skills)) * 100
    return round(score, 2)

# Function to extract candidate name (improved)
def extract_name(resume_text):
    """Attempts to extract a candidate's name from the resume."""
    print(f"Resume Text Preview: {resume_text[:500]}")  # Print first 500 characters to debug

    # Common patterns for name extraction (including cases with initials, etc.)
    name_pattern = r'^[A-Z][a-z]+(?: [A-Z][a-z]+)+$'  # Matches names like 'John Doe' or 'John M. Doe'
    
    # Step 1: Check the first few lines of the resume for name-like patterns
    lines = resume_text.split('\n')
    
    # Check the first few lines (usually the name appears at the top)
    for line in lines[:5]:  # Check the first 5 lines for name-like patterns
        line = line.strip()
        if re.match(name_pattern, line):
            return line.strip()

    # Step 2: If not found, check for keywords like "Name", "Contact", or "Resume"
    for line in lines:
        line = line.strip().lower()
        if "name" in line:  # If "Name" keyword appears, extract the name after it
            parts = line.split(":")
            if len(parts) > 1:
                return parts[1].strip()  # Take the portion after 'Name:'

    # Step 3: Try to extract names based on typical formatting like "John Doe"
    name_candidates = re.findall(r'[A-Z][a-z]+(?: [A-Z][a-z]+)+', resume_text)
    if name_candidates:
        return name_candidates[0].strip()  # Return the first matching name

    # If still no valid name found, return a default name
    return "Name Not Found"

# Home route
@app.route('/')
def home():
    return "AI Resume Screening API is running!"

# Predict route
@app.route('/predict', methods=['POST'])
def predict():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        # Extract and preprocess resume text
        resume_text = extract_text_from_resume(file)
        preprocessed_text = preprocess_text(resume_text)

        # Make a prediction using the trained model (predict job role)
        job_prediction = model.predict([preprocessed_text])[0]

        # You can calculate the qualification score based on the model's prediction
        # Example: You can map your AI predictions to skills dynamically by using a similar logic
        # Let's assume your model predicts the role 'data_analyst', you could map the skills dynamically
        job_profiles = {
            "data_analyst": ["python", "sql", "excel", "data analysis", "statistics", "machine learning"],
            "software_engineer": ["java", "c++", "spring", "angular", "javascript", "development"],
            "web_developer": ["html", "css", "javascript", "react", "angular", "web design"],
            "project_manager": ["management", "leadership", "agile", "scrum", "planning", "risk management"]
        }

        # Get skills based on the predicted job role
        skills = job_profiles.get(job_prediction, [])
        qualification_score = calculate_score(resume_text, skills)

        # Extract the candidate's name
        candidate_name = extract_name(resume_text)

        # Extract qualifications (skills)
        qualifications = [skill for skill in skills if skill in resume_text.lower()]

        return jsonify({
            'name': candidate_name,
            'job_description': job_prediction,  # AI model predicts this job
            'qualifications': qualifications,
            'resume_score': f"{qualification_score}%"  # Assuming score as a percentage
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':  
    app.run(debug=True)
