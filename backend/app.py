from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import docx
import PyPDF2

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        
        file = request.files['resume']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        resume_text = ""

        if file.filename.lower().endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                resume_text += page.extract_text() or ''
        elif file.filename.lower().endswith('.docx'):
            doc = docx.Document(file)
            resume_text = '\n'.join([para.text for para in doc.paragraphs])
        else:
            return jsonify({'error': 'Unsupported file format'}), 400
        
        # Trim resume text for display
        resume_preview = resume_text[:500]  # Show the first 500 characters
        
        # Include the preview in the response
        result = {
            "job_description": "data_analyst",
            "name": "Consultant Business Analyst",
            "qualifications": ["sql", "excel", "data analysis"],
            "resume_score": "16.67%",
            "resume_preview": resume_preview  # Add this line
        }

        return jsonify(result)

    except Exception as e:
        print("Error while processing resume:", e)
        return jsonify({'error': 'An error occurred while processing the resume'}), 500

if __name__ == '__main__':
    app.run(debug=True)
