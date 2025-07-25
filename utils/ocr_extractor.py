from pdf2image import convert_from_path
import easyocr
import numpy as np
import os
import re

def clean_text(text):
    """Clean extracted text to remove common OCR artifacts."""
    
    text = re.sub(r'\s+', ' ', text)
    
    text = re.sub(r'[^\w\s।!?]', '', text)
    return text.strip()

def extract_text_from_fixed_pdf(pdf_path="uploads/uploads\HSC26-Bangla1st-Paper.pdf", output_txt="Extracted_text.txt"):
    
    pdf_path = os.path.abspath(pdf_path)

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found at: {pdf_path}. Please check the file path or ensure the file exists.")

    try:
        print("Converting PDF to images...")
        pages = convert_from_path(pdf_path, dpi=300)
        reader = easyocr.Reader(['en', 'bn'])  
        all_text = ""

        for i, page in enumerate(pages, 1):
            print(f"Processing page {i} of {len(pages)}")
            img = np.array(page)
            
            text_lines = reader.readtext(img, detail=0, paragraph=True)
            text = "\n".join(text_lines)
            all_text += text + "\n\n"

        
        all_text = clean_text(all_text)

        with open(output_txt, "w", encoding="utf-8") as f:
            f.write(all_text)
        print(f"Text extracted and saved to {output_txt}")
        return all_text

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return ""