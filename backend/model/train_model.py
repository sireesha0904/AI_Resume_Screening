import os
import pandas as pd
import docx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# Path to dataset CSV
csv_file = r"C:\Users\modis\Documents\AI_Resume_Screening\data\dataset.csv"

# Load dataset
df = pd.read_csv(csv_file)

# Convert paths to absolute if needed
df['filename'] = df['filename'].apply(
    lambda x: os.path.join(r"C:\Users\modis\Documents\AI_Resume_Screening", x.replace("/", "\\"))
)

# Function to extract text from DOCX files
def read_docx(file_path):
    try:
        doc = docx.Document(file_path)
        full_text = [para.text for para in doc.paragraphs]
        return ' '.join(full_text)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ''

# Read text from resumes
df['text'] = df['filename'].apply(read_docx)
df = df[df['text'].str.strip() != '']  # remove empty records

# Features and labels
X = df['text'].values
y = df['label'].values

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X_tfidf = vectorizer.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)

# Logistic Regression model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Classification Report
report = classification_report(y_test, y_pred)
print(report)

# Save classification report to file
with open(r"C:\Users\modis\Documents\AI_Resume_Screening\backend\model\classification_report.txt", "w") as f:
    f.write(report)

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.savefig(r"C:\Users\modis\Documents\AI_Resume_Screening\backend\model\confusion_matrix.png")
plt.show()

# Save model and vectorizer
joblib.dump(model, r"C:\Users\modis\Documents\AI_Resume_Screening\backend\model\resume_model.pkl")
joblib.dump(vectorizer, r"C:\Users\modis\Documents\AI_Resume_Screening\backend\model\tfidf_vectorizer.pkl")

print("✅ Model, vectorizer, classification report, and confusion matrix saved successfully!")
