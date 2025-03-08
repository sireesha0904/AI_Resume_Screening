# app.py
from flask import Flask, request, jsonify
from utils.preprocess import preprocess_text
from utils.text_extractor import extract_text_from_resume
import pandas as pd
import os
import pickle

app = Flask(__name__)

# Load the trained model
model_path = os.path.join(os.path.dirname(__file__), 'model', 'resume_model.pkl')
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# Endpoint for resume screening
@app.route('/screen', methods=['POST'])
def screen_resume():
    file = request.files['resume']
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400
    resume_text = extract_text_from_resume(file)
    if not resume_text:
        return jsonify({'error': 'Could not extract text from resume'}), 400
    processed_text = preprocess_text(resume_text)
    prediction = model.predict([processed_text])[0]
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True)