from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.schemas.ocr import OCRProcessResponse
from app.services.ocr_service import OCRService

router = APIRouter()

@router.post("/ocr/process", response_model=OCRProcessResponse)
async def process_ocr(
    file: UploadFile = File(...),
    documentId: str = Form("doc-auto"),
    forceOcr: bool = Form(False)
):
    try:
        file_bytes = await file.read()
        if not file_bytes:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")
            
        filename = file.filename or "uploaded_document.pdf"
        result = OCRService.process_document(
            file_bytes=file_bytes,
            filename=filename,
            document_id=documentId,
            force_ocr=forceOcr
        )
        return result
        
    except Exception as e:
        print(f"[OCR Route Error] {e}")
        raise HTTPException(status_code=500, detail=str(e))
