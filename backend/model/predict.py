import pickle
from backend.utils.text_extractor import extract_text_from_resume
from backend.utils.preprocess import preprocess_text

# Load the trained model and vectorizer
model_path = "backend/model/resume_model.pkl"
vectorizer_path = "backend/model/vectorizer.pkl"

with open(model_path, "rb") as f:
    model = pickle.load(f)

with open(vectorizer_path, "rb") as f:
    vectorizer = pickle.load(f)

def predict_resume(resume_text):
    processed_text = preprocess_text(resume_text)
    vectorized_text = vectorizer.transform([processed_text])
    prediction = model.predict(vectorized_text)
    return prediction[0]  # Return predicted label
