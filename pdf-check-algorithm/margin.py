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

def extract_text_with_positions(image):
    """
    Extract text from an image using OCR and get positions of each text box.
    """
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    text_positions = []
    n_boxes = len(data['level'])
    for i in range(n_boxes):
        text = data['text'][i]
        if text.strip() != "":
            (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            text_positions.append((text.strip(), (x, y, x + w, y + h)))
    return text_positions

def detect_page_number(text_positions):
    """
    Detect page numbers in the text using regular expressions and return their positions.
    """
    patterns = [
        r'^\d+$',  # Matches a single number
        r'^\d+\s*of\s*\d+$',  # Matches patterns like '1 of 2'
        r'^Page\s*\d+$',  # Matches patterns like 'Page 1'
        r'^Page\s*\d+\s*of\s*\d+$'  # Matches patterns like 'Page 1 of 2'
    ]
    potential_page_numbers = []

    for text, (x1, y1, x2, y2) in text_positions:
        for pattern in patterns:
            if re.match(pattern, text, re.IGNORECASE):
                potential_page_numbers.append((text, (x1, y1, x2, y2)))
                break

    return potential_page_numbers

def detect_margins(image):
    """
    Detect the margins of text in the image.
    """
    h, w = image.shape[:2]
    ocr_result = pytesseract.image_to_boxes(image)
    margins = {'top': h, 'bottom': h, 'left': w, 'right': w}
    
    for box in ocr_result.splitlines():
        b = box.split()
        x, y, x2, y2 = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        margins['top'] = min(margins['top'], h - y2)
        margins['bottom'] = min(margins['bottom'], y)
        margins['left'] = min(margins['left'], x)
        margins['right'] = min(margins['right'], w - x2)
    
    return margins

def draw_margins(image, margins):
    """
    Draw margins on the image.
    """
    h, w = image.shape[:2]
    top, bottom, left, right = margins['top'], margins['bottom'], margins['left'], margins['right']
    
    # Draw rectangles representing the margins
    cv2.rectangle(image, (0, h - top), (w, h), (0, 255, 0), 2)  # Top margin
    cv2.rectangle(image, (0, 0), (w, bottom), (255, 0, 0), 2)   # Bottom margin
    cv2.rectangle(image, (0, 0), (left, h), (0, 0, 255), 2)     # Left margin
    cv2.rectangle(image, (w - right, 0), (w, h), (255, 255, 0), 2)  # Right margin
    
    return image

# Example usage
pdf_path = './testing/Hostel.pdf'

# Convert PDF to images
images = convert_pdf_to_images(pdf_path)

# Process each image
for page_num, image in enumerate(images):
    # Extract text with positions from the image
    text_positions = extract_text_with_positions(image)
    
    # Detect page number in the text positions
    page_numbers = detect_page_number(text_positions)
    
    print(f"Page numbers detected on page {page_num + 1}: {page_numbers}")
    
    # Detect margins
    margins = detect_margins(image)
    print(f"Page {page_num + 1} margins: {margins}")
    
    # Draw margins on the image
    image_with_margins = draw_margins(image.copy(), margins)
    
    # Visualize the page numbers
    for text, (x1, y1, x2, y2) in page_numbers:
        cv2.rectangle(image_with_margins, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image_with_margins, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    # Display the image with detected page numbers and margins
    cv2.imshow(f'Page {page_num + 1}', image_with_margins)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
