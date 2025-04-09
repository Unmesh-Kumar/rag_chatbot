import fitz
from docx import Document
from pathlib import Path
from .constants import INSURANCE_DOC_DIR, PDF_EXTENSION, DOCX_EXTENSION, NEWLINE, TEXT_KEY, METADATA_KEY, SOURCE_KEY


def extract_text_from_pdf(path):
   doc = fitz.open(path)
   return "".join([page.get_text() for page in doc])

def extract_text_from_docx(path):
   doc = Document(path)
   return NEWLINE.join([para.text for para in doc.paragraphs])

def load_documents(dir_path=INSURANCE_DOC_DIR):
   docs = []
   for file_path in Path(dir_path).glob("*"):
      if file_path.suffix == PDF_EXTENSION:
         text = extract_text_from_pdf(file_path)
      elif file_path.suffix == DOCX_EXTENSION:
         text = extract_text_from_docx(file_path)
      else:
         continue
         
      if not text.strip():
         continue
         
      docs.append({
         TEXT_KEY: text,
         METADATA_KEY: {
         SOURCE_KEY: file_path.name
         }
      })
   
   return docs