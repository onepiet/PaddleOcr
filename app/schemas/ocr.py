from typing import List, Optional, Any
from pydantic import BaseModel, Field

class OCRBlock(BaseModel):
    text: str = Field(..., description="Recognized text snippet")
    confidence: float = Field(..., ge=0.0, le=1.0, description="OCR engine confidence score")
    bbox: List[float] = Field(..., description="Bounding box coordinates [x1, y1, x2, y2]")

class OCRPage(BaseModel):
    page_number: int = Field(..., description="1-indexed page number")
    text: str = Field(..., description="Normalized full text for page")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Average confidence score for page")
    source: str = Field("OCR", description="Source of extraction: 'PDF_TEXT' or 'OCR'")
    blocks: List[OCRBlock] = Field(default_factory=list, description="Text blocks with bounding boxes")

class OCRProcessResponse(BaseModel):
    success: bool = True
    document_id: str = Field(..., description="Original Document ID")
    pages: List[OCRPage] = Field(default_factory=list)
    full_text: str = Field("", description="Complete extracted text across all pages")
    overall_confidence: float = Field(0.90, description="Overall weighted confidence score")
    total_pages: int = Field(0, description="Total number of pages processed")
    engine: str = Field("PaddleOCR", description="Primary OCR Engine Used")
    engine_version: str = Field("v3.7.0", description="OCR Engine Version")
    processing_time_ms: float = Field(0.0, description="Processing duration in milliseconds")
    error: Optional[str] = None

class HealthCheckResponse(BaseModel):
    status: str = "ok"
    ocr: str = "available"
    engine: str = "PaddleOCR"
    version: str = "v3.7.0"
    device: str = "cpu"
