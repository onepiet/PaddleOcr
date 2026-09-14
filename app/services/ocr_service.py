import time
from typing import List, Dict, Any, Tuple
from app.config import settings
from app.schemas.ocr import OCRBlock, OCRPage, OCRProcessResponse
from app.services.pdf_service import PDFService
from app.services.preprocessing import convert_bytes_to_cv2_image, preprocess_image_for_ocr

class OCRService:
    _ocr_engine = None

    @classmethod
    def get_ocr_engine(cls):
        if cls._ocr_engine is None:
            try:
                from paddleocr import PaddleOCR
                print(f"[OCRService] Initializing PaddleOCR Engine (lang={settings.DEFAULT_LANG})...")
                cls._ocr_engine = PaddleOCR(lang=settings.DEFAULT_LANG)
            except Exception as err:
                print(f"[OCRService] Error instantiating PaddleOCR: {err}")
                raise err
        return cls._ocr_engine

    @classmethod
    def process_image_bytes(cls, img_bytes: bytes) -> Tuple[str, float, List[Dict[str, Any]]]:
        img = convert_bytes_to_cv2_image(img_bytes)
        if img is None:
            return "", 0.0, []

        engine = cls.get_ocr_engine()
        result = engine.ocr(img, cls=True)

        text_snippets = []
        blocks = []
        total_conf = 0.0
        count = 0

        if result and len(result) > 0 and result[0]:
            for line in result[0]:
                box = line[0]  # [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
                text, conf = line[1]

                x_coords = [p[0] for p in box]
                y_coords = [p[1] for p in box]
                bbox = [
                    round(float(min(x_coords)), 1),
                    round(float(min(y_coords)), 1),
                    round(float(max(x_coords)), 1),
                    round(float(max(y_coords)), 1)
                ]

                clean_t = text.strip()
                if clean_t:
                    text_snippets.append(clean_t)
                    blocks.append({
                        "text": clean_t,
                        "confidence": round(float(conf), 3),
                        "bbox": bbox
                    })
                    total_conf += float(conf)
                    count += 1

        avg_conf = round(total_conf / count, 3) if count > 0 else 0.85
        full_text = "\n".join(text_snippets)
        return full_text, avg_conf, blocks

    @classmethod
    def process_document(cls, file_bytes: bytes, filename: str, document_id: str, force_ocr: bool = False) -> OCRProcessResponse:
        start_time = time.time()
        lower_filename = filename.lower()

        if lower_filename.endswith(".pdf"):
            page_count, pdf_pages, is_digital_text = PDFService.inspect_pdf(file_bytes)

            if is_digital_text and not force_ocr:
                # Route A: Digital Text PDF -> Extract text directly via PyMuPDF/pdf-parse
                pages: List[OCRPage] = []
                all_texts = []
                for p in pdf_pages:
                    pages.append(
                        OCRPage(
                            page_number=p["page_number"],
                            text=p["text"],
                            confidence=0.96,
                            source="PDF_TEXT",
                            blocks=[]
                        )
                    )
                    all_texts.append(p["text"])

                full_text = "\n\n".join(all_texts)
                duration_ms = round((time.time() - start_time) * 1000, 2)

                return OCRProcessResponse(
                    success=True,
                    document_id=document_id,
                    pages=pages,
                    full_text=full_text,
                    overall_confidence=0.96,
                    total_pages=page_count,
                    engine="PyMuPDF / TextParser",
                    engine_version="v1.23",
                    processing_time_ms=duration_ms
                )

            else:
                # Route B: Scanned PDF -> Render pages as images and execute PaddleOCR
                pages: List[OCRPage] = []
                all_texts = []
                total_conf = 0.0

                for page_num in range(1, page_count + 1):
                    img_bytes = PDFService.render_pdf_page_to_image_bytes(file_bytes, page_num, dpi=settings.OCR_DPI)
                    p_text, p_conf, p_blocks = cls.process_image_bytes(img_bytes)

                    ocr_blocks = [OCRBlock(**b) for b in p_blocks]
                    pages.append(
                        OCRPage(
                            page_number=page_num,
                            text=p_text,
                            confidence=p_conf,
                            source="OCR",
                            blocks=ocr_blocks
                        )
                    )
                    all_texts.append(p_text)
                    total_conf += p_conf

                avg_conf = round(total_conf / max(1, page_count), 3)
                full_text = "\n\n".join(all_texts)
                duration_ms = round((time.time() - start_time) * 1000, 2)

                return OCRProcessResponse(
                    success=True,
                    document_id=document_id,
                    pages=pages,
                    full_text=full_text,
                    overall_confidence=avg_conf,
                    total_pages=page_count,
                    engine="PaddleOCR",
                    engine_version="v3.7.0",
                    processing_time_ms=duration_ms
                )

        else:
            # Image Document (PNG, JPG, JPEG, WEBP, etc.)
            p_text, p_conf, p_blocks = cls.process_image_bytes(file_bytes)
            ocr_blocks = [OCRBlock(**b) for b in p_blocks]

            page = OCRPage(
                page_number=1,
                text=p_text,
                confidence=p_conf,
                source="OCR",
                blocks=ocr_blocks
            )

            duration_ms = round((time.time() - start_time) * 1000, 2)
            return OCRProcessResponse(
                success=True,
                document_id=document_id,
                pages=[page],
                full_text=p_text,
                overall_confidence=p_conf,
                total_pages=1,
                engine="PaddleOCR",
                engine_version="v3.7.0",
                processing_time_ms=duration_ms
            )
