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

# Define skill sets for each job role
job_profiles = {
    "data_analyst": ["python", "sql", "excel", "data analysis", "statistics", "machine learning"],
    "software_engineer": ["java", "c++", "spring", "angular", "javascript", "development"],
    "web_developer": ["html", "css", "javascript", "react", "angular", "web design"],
    "project_manager": ["management", "leadership", "agile", "scrum", "planning", "risk management"]
}

# Function to calculate the qualification score
def calculate_score(resume_text, skills):
    resume_words = re.findall(r'\w+', resume_text.lower())
    resume_counter = Counter(resume_words)
    matched_skills = [skill for skill in skills if skill in resume_counter]
    score = (len(matched_skills) / len(skills)) * 100
    return round(score, 2)

# Function to extract candidate name (simple heuristic)
def extract_name(resume_text):
    lines = resume_text.split('\n')
    for line in lines:
        line = line.strip()
        if re.match(r'^[A-Z][a-z]* [A-Z][a-z]*$', line):
            return line
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

        # Make a prediction using the trained model
        prediction = model.predict([preprocessed_text])[0]

        # Calculate the qualification score
        qualification_score = calculate_score(resume_text, job_profiles.get(prediction, []))

        # Extract the candidate's name
        candidate_name = extract_name(resume_text)

        return jsonify({
            'name': candidate_name,
            'job_description': prediction,
            'qualification_score': qualification_score,
            'resume_score': f"{qualification_score}%"  # Assuming score as a percentage
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
