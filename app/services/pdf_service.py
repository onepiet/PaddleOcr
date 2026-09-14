import pymupdf as fitz
import io
import re
from typing import List, Tuple, Dict, Any
from app.config import settings

class PDFService:
    @staticmethod
    def inspect_pdf(pdf_bytes: bytes) -> Tuple[int, List[Dict[str, Any]], bool]:
        """
        Inspects PDF document using PyMuPDF:
        - Returns page count
        - Extracts text per page
        - Applies text-detection heuristic to classify as Digital Text vs Scanned Image PDF
        """
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page_count = len(doc)
        pages_data = []
        total_text_length = 0
        printable_char_count = 0

        for idx, page in enumerate(doc):
            page_text = page.get_text("text") or ""
            clean_text = page_text.strip()
            total_text_length += len(clean_text)
            
            # Count printable alphanumeric characters
            alphanumeric = len(re.findall(r'[A-Za-z0-9]', clean_text))
            printable_char_count += alphanumeric
            
            pages_data.append({
                "page_number": idx + 1,
                "text": clean_text,
                "length": len(clean_text),
                "alphanumeric_count": alphanumeric
            })

        doc.close()

        # Heuristic Rule for Digital Text vs Scanned Image:
        # 1. Total alphanumeric characters >= MIN_CHAR_COUNT (default 50)
        # 2. Average alphanumeric density per page >= MIN_CHAR_DENSITY_PER_PAGE (default 40)
        avg_density = printable_char_count / max(1, page_count)
        is_digital_text = (printable_char_count >= settings.MIN_CHAR_COUNT) and (avg_density >= settings.MIN_CHAR_DENSITY_PER_PAGE)

        return page_count, pages_data, is_digital_text

    @staticmethod
    def render_pdf_page_to_image_bytes(pdf_bytes: bytes, page_number: int, dpi: int = 200) -> bytes:
        """
        Renders a specific page of PDF to image bytes (PNG) at specified DPI.
        """
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        if page_number < 1 or page_number > len(doc):
            doc.close()
            raise ValueError(f"Page number {page_number} out of bounds (1-{len(doc)})")
        
        page = doc[page_number - 1]
        zoom = dpi / 72.0
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        
        img_bytes = pix.tobytes("png")
        doc.close()
        return img_bytes
