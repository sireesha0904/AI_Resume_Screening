# train_model.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# Load dataset
df = pd.read_csv('data/dataset.csv')
X = df['job_description_text'].fillna('')
y = df['job_title']

# Vectorize text data
vectorizer = TfidfVectorizer(stop_words='english')
X_vectorized = vectorizer.fit_transform(X)

# Train the model
model = MultinomialNB()
model.fit(X_vectorized, y)

# Save the model
model_path = 'model/resume_model.pkl'
with open(model_path, 'wb') as f:
    pickle.dump(model, f)

print('Model trained and saved successfully!')
