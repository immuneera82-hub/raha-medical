# Report Processing Service
# Extracts text from PDFs and images to identify medical test types

import io
import os
import tempfile
from typing import Optional
from PIL import Image

# OCR and PDF libraries
try:
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

try:
    from PyPDF2 import PdfReader
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    from pdf2image import convert_from_bytes
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False

from medical_keywords import extract_test_name, generate_report_name, get_file_extension


# Tesseract configuration for Arabic + English
TESSERACT_CONFIG = '--oem 3 --psm 3'
TESSERACT_LANG = 'ara+eng'


def extract_text_from_image(image_bytes: bytes) -> str:
    """Extract text from image using OCR."""
    if not OCR_AVAILABLE:
        return ""
    
    try:
        image = Image.open(io.BytesIO(image_bytes))
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        text = pytesseract.image_to_string(
            image, 
            lang=TESSERACT_LANG,
            config=TESSERACT_CONFIG
        )
        return text
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract text from PDF file."""
    text = ""
    
    # Try direct text extraction first
    if PDF_AVAILABLE:
        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            for page in reader.pages[:5]:  # Limit to first 5 pages
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            print(f"PDF Text Extraction Error: {e}")
    
    # If no text found, try OCR on PDF images
    if not text.strip() and PDF2IMAGE_AVAILABLE and OCR_AVAILABLE:
        try:
            images = convert_from_bytes(pdf_bytes, first_page=1, last_page=2)
            for img in images:
                img_text = pytesseract.image_to_string(
                    img,
                    lang=TESSERACT_LANG,
                    config=TESSERACT_CONFIG
                )
                text += img_text + "\n"
        except Exception as e:
            print(f"PDF OCR Error: {e}")
    
    return text


def process_report(file_bytes: bytes, filename: str, patient_code: str) -> dict:
    """
    Process a medical report file and generate an appropriate name.
    
    Args:
        file_bytes: The file content as bytes
        filename: Original filename
        patient_code: Patient's unique code (e.g., Raha-XXXXX)
    
    Returns:
        dict with 'original_name', 'new_name', 'test_type', 'success'
    """
    extension = get_file_extension(filename)
    extracted_text = ""
    
    # Extract text based on file type
    if extension == 'pdf':
        extracted_text = extract_text_from_pdf(file_bytes)
    elif extension in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp']:
        extracted_text = extract_text_from_image(file_bytes)
    
    # Identify the test type
    test_name = extract_test_name(extracted_text)
    
    # Generate new filename
    new_name = generate_report_name(test_name, patient_code, extension)
    
    return {
        'original_name': filename,
        'new_name': new_name,
        'test_type': test_name,
        'extracted_text_preview': extracted_text[:200] if extracted_text else "",
        'success': True
    }


def get_test_type_from_text(text: str) -> str:
    """Simple wrapper to get test type from text."""
    return extract_test_name(text)
