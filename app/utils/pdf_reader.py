from pdfminer.high_level import extract_text
from fastapi import UploadFile
import tempfile

def extract_text_from_pdf(upload_file: UploadFile) -> str:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(upload_file.file.read())
            tmp.flush()
            text = extract_text(tmp.name)
        return text.strip()
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF '{upload_file.filename}': {e}")
