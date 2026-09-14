from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health, ocr
from app.config import settings

app = FastAPI(
    title="BIDSETU AI & OCR Service",
    description="Production-grade PaddleOCR & PyMuPDF document intelligence microservice for BIDSETU",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(ocr.router)

@app.get("/")
async def root():
    return {
        "service": "BIDSETU AI & OCR Service",
        "version": "1.0.0",
        "status": "running",
        "engine": "PaddleOCR v3.7.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=False)
