"""
Resume file parser for PDF and TXT resumes using PyMuPDF (fitz).
- Securely extracts text and images from PDF or TXT files for pipeline ingestion.
- Input: file-like object (e.g., UploadFile.file or BytesIO)
- Output: extracted plain text (str) and optional image paths (list)
"""

import io
import os
import fitz  # PyMuPDF
from typing import BinaryIO


def extract_resume_text(file: BinaryIO, filename: str) -> str:
    """
    Extracts text from a PDF or TXT resume file using fitz.
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
            doc = fitz.open(stream=file, filetype="pdf")
            text = "\n".join([page.get_text() for page in doc])
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


def extract_images_from_pdf(file: BinaryIO, output_dir: str = "images") -> list[str]:
    doc = fitz.open(stream=file, filetype="pdf")
    image_paths = []

    os.makedirs(output_dir, exist_ok=True)

    for page_index in range(len(doc)):
        for img_index, img in enumerate(doc[page_index].get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = f"{output_dir}/page{page_index+1}_img{img_index+1}.{image_ext}"

            with open(image_filename, "wb") as f:
                f.write(image_bytes)
            image_paths.append(image_filename)

    return image_paths


# ------------ CLI Test Runner ------------
if __name__ == "__main__":
    test_files = [
        ("SampleResumeHack.pdf", "application/pdf"),
        ("SampleResumeHack.txt", "text/plain"),
    ]

    for file_path, file_type in test_files:
        try:
            with open(file_path, "rb") as f:
                content = extract_resume_text(f.read(), file_path)
                print(f"\n✅ Extracted text from {file_path}:\n")
                print(content[:1000])  # Limit preview to 1000 chars
        except Exception as e:
            print(f"\n❌ Error processing {file_path}: {e}")
