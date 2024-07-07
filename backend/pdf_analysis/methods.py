from django.http import HttpResponse
import pytesseract
import fitz
from PIL  import Image
from pdf2image import convert_from_path
import cv2
import numpy as np
import re




class PDFAnalysis:
    def __init__(self, pdf, top, bottom ,left, right):
        self.pdf = pdf
        self.pdf_path = pdf.pdf.path
        self.top  = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.image = None

    def convert_pdf_to_images(self):
        pages = convert_from_path(self.pdf_path, 300)  # Adjust dpi as needed
        images = [cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR) for page in pages]
        self.image = images

    def extract_text(self, image):
        text = pytesseract.image_to_string(image)
        return text
    def check_blank_pages(self):
        return HttpResponse("Check Blank Pages functionality")

    def detect_page_number_location(self):
        # Implement the logic for detecting page number location
        return HttpResponse("Detect Page Number Location functionality")

    def find_landscape_pages(self):
        # Implement the logic for finding landscape pages
        return HttpResponse("Find Landscape Pages functionality")

    def check_double_sided(self):
        # Implement the logic for checking if the PDF is double-sided
        return HttpResponse("Check if PDF is Double-Sided functionality")

    def verify_margin_specification(self, top_margin, left_margin, bottom_margin, right_margin):
        # Implement the logic for verifying margin specifications
        return HttpResponse("Check and Verify Margin Specification functionality")

    def perform_all_functions(self, top_margin, left_margin, bottom_margin, right_margin):
        # Call all the functions
        self.check_blank_pages()
        self.detect_page_number_location()
        self.find_landscape_pages()
        self.check_double_sided()
        self.verify_margin_specification(top_margin, left_margin, bottom_margin, right_margin)
        return HttpResponse("Perform All Functions functionality")
