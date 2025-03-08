import os
import pandas as pd
from docx import Document

# Define the paths
resumes_folder = '../../data/resumes'
csv_file = '../../data/dataset.csv'
output_folder = '../../data/job_descriptions'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load the CSV file
df = pd.read_csv(csv_file)

# Check if required columns exist in the CSV
if 'filename' not in df.columns or 'label' not in df.columns:
    print("Error: 'filename' and 'label' columns are required in the CSV file.")
    exit()

# Process each file in the resumes folder
for filename in os.listdir(resumes_folder):
    if filename.endswith('.docx'):
        file_path = os.path.join(resumes_folder, filename)

        # Read the document content
        doc = Document(file_path)
        full_text = []
        for paragraph in doc.paragraphs:
            full_text.append(paragraph.text)
        text = '\n'.join(full_text)

        # Check if the filename exists in the CSV
        matching_rows = df.loc[df['filename'] == filename, 'label']
        if not matching_rows.empty:
            label = matching_rows.values[0]
            output_filename = f"{os.path.splitext(filename)[0]}_{label}.txt"
            output_path = os.path.join(output_folder, output_filename)

            # Save the text content to a .txt file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Processed and saved: {output_filename}")
        else:
            print(f"Warning: Filename '{filename}' not found in the CSV file.")
