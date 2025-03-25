import os
import pandas as pd
import docx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Path to dataset
csv_file = r"C:\Users\modis\Documents\AI_Resume_Screening\data\dataset.csv"

# Load CSV
df = pd.read_csv(csv_file)

# Convert relative paths to absolute paths if needed
df['filename'] = df['filename'].apply(
    lambda x: os.path.join(r"C:\Users\modis\Documents\AI_Resume_Screening", x.replace("/", "\\"))
)

# Function to read text from DOCX
def read_docx(file_path):
    try:
        doc = docx.Document(file_path)
        full_text = [para.text for para in doc.paragraphs]
        return ' '.join(full_text)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ''

# Read resume texts
df['text'] = df['filename'].apply(read_docx)

# Remove entries where text is empty
df = df[df['text'].str.strip() != '']

# Features & Labels
X = df['text'].values
y = df['label'].values

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X_tfidf = vectorizer.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model & vectorizer
joblib.dump(model, r"C:\Users\modis\Documents\AI_Resume_Screening\backend\model\resume_model.pkl")
joblib.dump(vectorizer, r"C:\Users\modis\Documents\AI_Resume_Screening\backend\model\tfidf_vectorizer.pkl")

print("Model and vectorizer saved successfully!")
