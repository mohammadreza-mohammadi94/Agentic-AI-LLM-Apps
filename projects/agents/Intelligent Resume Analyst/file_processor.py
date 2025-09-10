# /file_processor.py
"""
This module has a single responsibility: extracting text from PDF files.
"""
from typing import IO, Optional
import pypdf

def extract_text_from_pdf(pdf_file: IO[bytes]) -> Optional[str]:
    """
    Extracts text content from an uploaded PDF file object.
    """
    try:
        reader = pypdf.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        # Return the text or a specific message if no text was found
        return text.strip() if text else "Could not extract any text from the PDF."
    except Exception as e:
        print(f"Error processing PDF file: {e}")
        return None
    