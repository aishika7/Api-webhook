import fitz  # PyMuPDF
from docx import Document
from typing import List, Tuple
import os

def extract_text_from_pdf(path: str) -> List[Tuple[int, str]]:
    doc = fitz.open(path)
    pages = []
    for i, page in enumerate(doc, start=1):
        try:
            txt = page.get_text("text")
        except Exception:
            txt = ''
        pages.append((i, txt.strip()))
    return pages

def extract_text_from_docx(path: str):
    doc = Document(path)
    full = []
    for p in doc.paragraphs:
        full.append(p.text)
    return [(1, '\n'.join(full))]
