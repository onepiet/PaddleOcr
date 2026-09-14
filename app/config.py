import os
from pydantic import BaseModel

class Settings(BaseModel):
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    
    # OCR Engine settings
    USE_GPU: bool = os.getenv("USE_GPU", "false").lower() == "true"
    DEFAULT_LANG: str = os.getenv("DEFAULT_LANG", "en")
    USE_ANGLE_CLS: bool = os.getenv("USE_ANGLE_CLS", "true").lower() == "true"
    
    # Text Extraction Heuristic Thresholds
    MIN_CHAR_COUNT: int = int(os.getenv("MIN_CHAR_COUNT", "50"))
    MIN_CHAR_DENSITY_PER_PAGE: int = int(os.getenv("MIN_CHAR_DENSITY_PER_PAGE", "40"))
    OCR_DPI: int = int(os.getenv("OCR_DPI", "200"))
    
    # Processing Limits
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "50"))
    MAX_PAGES: int = int(os.getenv("MAX_PAGES", "100"))
    OCR_TIMEOUT_SECONDS: int = int(os.getenv("OCR_TIMEOUT_SECONDS", "120"))

settings = Settings()
