import os
from typing import Dict, Any
from .pdf_parser import PDFParser
from .docx_parser import DOCXParser

class FileHandler:
    def __init__(self):
        self.pdf_parser = PDFParser()
        self.docx_parser = DOCXParser()

    def process(self, file_path: str) -> Dict[str, Any]:
        """Detects file type and processes it."""
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.pdf':
            return self.pdf_parser.extract_text(file_path)
        elif ext in ['.docx', '.doc']:
            return self.docx_parser.extract_text(file_path)
        elif ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return {"raw_text": f.read()}
        else:
            return {
                "raw_text": "",
                "error": f"Unsupported file format: {ext}"
            }
