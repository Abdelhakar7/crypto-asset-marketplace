import pdfplumber
import string
from io import BytesIO

#hashing pdf utils wkilek rbi ya roa 

def extract_text_from_pdf(content : bytes):
      
      with pdfplumber.open(BytesIO(content)) as pdf:
         
         first_page = pdf.pages[0]
         text = first_page.extract_text()
      return text

def extract_normalize_text(text):
    
    # Convert to lowercase
    text = text.lower()
    # Remove all whitespace (spaces, newlines, tabs)
    text = "".join(text.split())
    # Remove punctuation (optional: customize based on needs)
   
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text

def normalized_text(content : bytes) -> str:


      return  extract_normalize_text(extract_text_from_pdf(content))  