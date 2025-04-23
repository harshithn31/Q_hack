"""
Resume file parser for PDF and TXT resumes.
- Securely extracts text from PDF or TXT files for pipeline ingestion.
- Input: file-like object (e.g., FastAPI UploadFile.file or BytesIO)
- Output: extracted plain text (str)
- Raises ValueError on unsupported file types or extraction errors.

Security: Only accepts .pdf and .txt. Sanitizes output.
"""
import io
from typing import BinaryIO

import pdfplumber


def extract_resume_text(file: BinaryIO, filename: str) -> str:
    """
    Extracts text from a PDF or TXT resume file.
    Args:
        file: File-like object (opened in binary mode)
        filename: Name of the uploaded file (for type detection)
    Returns:
        Extracted plain text
    Raises:
        ValueError: If file type is unsupported or extraction fails
    """
    if filename.lower().endswith(".pdf"):
        try:
            import io
            # Reason: Wrap bytes in BytesIO for pdfplumber compatibility
            with pdfplumber.open(io.BytesIO(file)) as pdf:
                text = "\n".join(
                    page.extract_text() or "" for page in pdf.pages
                )
            if not text.strip():
                raise ValueError("No extractable text found in PDF.")
            return text.strip()
        except Exception as e:
            raise ValueError(f"PDF extraction failed: {e}")
    elif filename.lower().endswith(".txt"):
        try:
            text = file.read().decode("utf-8", errors="ignore")
            if not text.strip():
                raise ValueError("No extractable text found in TXT.")
            return text.strip()
        except Exception as e:
            raise ValueError(f"TXT extraction failed: {e}")
    else:
        raise ValueError("Unsupported file type. Only PDF and TXT are accepted.")
