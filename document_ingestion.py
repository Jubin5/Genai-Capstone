# document_ingestion.py
"""
Step 1: Document Ingestion
Extract text from PDF (using PyMuPDF) and DOCX, then save as TXT
"""

import os
import fitz  # PyMuPDF
from docx import Document


# --------- Function to extract text from PDF (PyMuPDF) ---------
def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text.strip()


# --------- Function to extract text from DOCX ---------
def extract_text_from_docx(docx_path: str) -> str:
    doc = Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    return text.strip()


# --------- Function to auto-detect and extract text ---------
def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Use PDF or DOCX.")


# --------- Function to save extracted text into .txt ---------
def save_to_txt(text: str, output_path: str):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)


# --------- Main Program ---------
if __name__ == "__main__":
    # Update file names with what you actually have
    pdf_file = "D:\GenAI Capstone Project\Samlpe policy.pdf"
    docx_file = "sample_policy.docx"   # optional

    # Extract from PDF
    if os.path.exists(pdf_file):
        pdf_text = extract_text(pdf_file)
        print("\n--- PDF Extracted Text (First 100000 chars) ---\n")
        print(pdf_text[:500])
        save_to_txt(pdf_text, "GovReport_extracted.txt")
        print(f"\n✅ Extracted text saved to GovReport_extracted.txt")
    else:
        print(f"{pdf_file} not found!")

    # Extract from DOCX (optional)
    if os.path.exists(docx_file):
        docx_text = extract_text(docx_file)
        print("\n--- DOCX Extracted Text (First 100000 chars) ---\n")
        print(docx_text[:500])
        save_to_txt(docx_text, "sample_policy_extracted.txt")
        print(f"\n✅ Extracted text saved to sample_policy_extracted.txt")
    else:
        print(f"{docx_file} not found!")

