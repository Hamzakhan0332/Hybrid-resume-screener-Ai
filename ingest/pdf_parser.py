import pdfplumber
import fitz  # PyMuPDF
from typing import Dict, Any, List

class PDFParser:
    def __init__(self):
        pass

    def extract_text(self, file_path: str) -> Dict[str, Any]:
        """
        Extracts text and layout information from a PDF file.
        Uses pdfplumber as primary and fitz as secondary.
        """
        results = {
            "raw_text": "",
            "pages": [],
            "metadata": {},
            "error": None
        }

        try:
            with pdfplumber.open(file_path) as pdf:
                full_text = []
                for i, page in enumerate(pdf.pages):
                    page_text = page.extract_text(layout=True)
                    if not page_text or len(page_text.strip()) < 10:
                        # Fallback to fitz if pdfplumber fails to get text (OCR might be needed)
                        page_text = self._fallback_extract(file_path, i)
                    
                    full_text.append(page_text)
                    results["pages"].append({
                        "page_number": i + 1,
                        "text": page_text,
                        "tables": page.extract_tables()
                    })
                
                results["raw_text"] = "\n".join(full_text)
                results["metadata"] = pdf.metadata

        except Exception as e:
            results["error"] = str(e)
        
        return results

    def _fallback_extract(self, file_path: str, page_index: int) -> str:
        """Fallback text extraction using PyMuPDF."""
        try:
            doc = fitz.open(file_path)
            page = doc.load_page(page_index)
            text = page.get_text("text")
            doc.close()
            return text
        except:
            return ""

if __name__ == "__main__":
    # Test logic
    import sys
    if len(sys.argv) > 1:
        parser = PDFParser()
        print(parser.extract_text(sys.argv[1])["raw_text"][:500])
