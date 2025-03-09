from flask import Flask, request, jsonify
import os
from utils.text_extractor import extract_text_from_resume
from utils.preprocess import preprocess_text
import pickle

app = Flask(__name__)

# Load the trained model
model_path = os.path.join(os.path.dirname(__file__), 'model', 'resume_model.pkl')
with open(model_path, 'rb') as f:
    model = pickle.load(f)
@app.route('/')
def home():
    return "AI Resume Screening API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['resume']
    resume_text = extract_text_from_resume(file)
    preprocessed_text = preprocess_text(resume_text)
    prediction = model.predict([preprocessed_text])
    return jsonify({'prediction': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
