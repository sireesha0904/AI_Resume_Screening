from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import pandas as pd
from utils.text_extractor import extract_text_from_resume
from utils.preprocess import preprocess_text

# Load your dataset
csv_file = "path_to_your_data/dataset.csv"
df = pd.read_csv(csv_file)

# Preprocess the text column and split dataset into features and labels
X = df['filename'].apply(extract_text_from_resume).apply(preprocess_text)
y = df['label']

# Convert text data to numerical features using TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
X_tfidf = vectorizer.fit_transform(X)

# Train a classifier
X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Evaluate the model
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

# Save the trained model to a file
import pickle
with open('resume_model.pkl', 'wb') as f:
    pickle.dump(clf, f)
