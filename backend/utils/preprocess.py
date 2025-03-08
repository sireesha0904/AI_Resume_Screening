import re

def preprocess_text(text):
    """Cleans and preprocesses the input text."""
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    text = re.sub(r'\W', ' ', text)  # Remove non-word characters
    return text.strip()
