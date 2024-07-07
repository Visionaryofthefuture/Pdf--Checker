import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np
import re

def convert_pdf_to_images(pdf_path):
    """
    Convert PDF pages to images.
    """
    pages = convert_from_path(pdf_path, 300)  # Adjust dpi as needed
    images = [cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR) for page in pages]
    return images

def extract_text(image):
    """
    Extract text from an image using OCR.
    """
    text = pytesseract.image_to_string(image)
    return text

def detect_page_number(text):
    """
    Detect page numbers in the text using regular expressions.
    """
    patterns = [
        r'^\d+$',  # Matches a single number
        r'^\d+\s*of\s*\d+$',  # Matches patterns like '1 of 2'
        r'^Page\s*\d+$',  # Matches patterns like 'Page 1'
        r'^Page\s*\d+\s*of\s*\d+$'  # Matches patterns like 'Page 1 of 2'
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group()

    return None

# Example usage
pdf_path = './testing/Hostel.pdf'

# Convert PDF to images
images = convert_pdf_to_images(pdf_path)

# Process each image
for page_num, image in enumerate(images):
    # Extract text from the image
    text = extract_text(image)
    
    # Detect page number in the text
    page_number = detect_page_number(text)
    
    print(f"Page numbers detected on page {page_num + 1}: {page_number}")

