import pdfplumber
import sys
import os

def extract_text(pdf_path):
    if not os.path.exists(pdf_path):
        return f"File not found: {pdf_path}"
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text += f"--- Page {i+1} ---\n{page_text}\n"
            return text
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    path = r"c:\Users\Mohammad Ukkasha\Desktop\FAST_API\CRUD_Operation\JWT ADMIN USER\LLm Intigration\AI Chat System\RAG System\data\TASK#4-Ai.pdf"
    print(extract_text(path))
