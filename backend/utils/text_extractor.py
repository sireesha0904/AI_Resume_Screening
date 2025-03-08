from docx import Document
import os

def extract_text_from_resume(file):
    """Extracts text from a .docx resume file."""
    temp_path = os.path.join(os.path.dirname(__file__), 'temp_resume.docx')
    with open(temp_path, 'wb') as temp_file:
        temp_file.write(file.read())

    document = Document(temp_path)
    resume_text = ' '.join([paragraph.text for paragraph in document.paragraphs])
    os.remove(temp_path)
    return resume_text.strip()
