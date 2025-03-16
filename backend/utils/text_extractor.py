from docx import Document
import os

def extract_text_from_resume(file):
    """Extracts text from a .docx resume file."""
    temp_path = os.path.join(os.path.dirname(__file__), 'temp_resume.docx')

    file.seek(0)  # Reset file pointer (for Flask uploads)
    with open(temp_path, 'wb') as temp_file:
        temp_file.write(file.read())

    document = Document(temp_path)

    # Extract paragraphs
    resume_text = []
    for para in document.paragraphs:
        resume_text.append(para.text)

    # Extract table data (if any)
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                resume_text.append(cell.text)

    os.remove(temp_path)  # Delete temp file

    extracted_text = ' '.join(resume_text).strip()
    print("Extracted Resume Text:", extracted_text[:500])  # Debug output
    return extracted_text
