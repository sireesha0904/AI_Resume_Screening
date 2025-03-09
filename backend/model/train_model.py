from dotenv import load_dotenv
import os
import pandas as pd
from backend.utils.text_extractor import extract_text_from_resume
from backend.utils.preprocess import preprocess_text
load_dotenv()

# Corrected file path pointing to the 'data' folder outside of 'backend'
csv_file = os.path.join(os.path.dirname(__file__), '../../data/dataset.csv')
absolute_path = os.path.abspath(csv_file)

# Debug: Show the expected path and list files in the directory
print("Expected Dataset Path:", absolute_path)
print("Files in data directory:", os.listdir(os.path.join(os.path.dirname(__file__), '../../data')))

if os.path.exists(absolute_path):
    print("✅ File found!")
    df = pd.read_csv(absolute_path)
    print(df.head())
else:
    print("❌ File not found! Check the file path and placement.")
