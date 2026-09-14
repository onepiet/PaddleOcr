---
title: BIDSETU PaddleOCR AI Service
emoji: 📑
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# BIDSETU — AI & PaddleOCR Document Intelligence Microservice

FastAPI microservice executing high-accuracy PaddleOCR, PyMuPDF text extraction, and bounding box layout analysis for BIDSETU (SIH26100 Procurement Verification Engine).

## Endpoints
- `GET /health`: Health diagnostic status
- `POST /ocr/process`: Multi-page PDF text & OCR bounding box extraction

## Environment Variables
- `PORT`: Service port (default 7860)
- `USE_ANGLE_CLS`: Enable text angle classification (`true`)
