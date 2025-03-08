# preprocess.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import re

vectorizer = TfidfVectorizer(stop_words='english')

def preprocess_text(text: str) -> str:
    # Basic text cleaning and preprocessing
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text.lower())
    return text

# Load and fit vectorizer on job descriptions
dataset_path = 'data/dataset.csv'
df = pd.read_csv(dataset_path)
if not df.empty and 'job_description_text' in df.columns:
    X = vectorizer.fit_transform(df['job_description_text'].fillna(''))
else:
    print('Dataset is empty or invalid column name!')

# text_extractor.py
import PyPDF2

def extract_text_from_resume(file) -> str:
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text() or ''
        return text.strip()
    except Exception as e:
        print(f'Error extracting text: {e}')
        return ''