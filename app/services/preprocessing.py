import cv2
import numpy as np

def convert_bytes_to_cv2_image(image_bytes: bytes) -> np.ndarray:
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def cv2_image_to_bytes(img: np.ndarray, ext: str = ".png") -> bytes:
    _, buf = cv2.imencode(ext, img)
    return buf.tobytes()

def preprocess_image_for_ocr(img: np.ndarray, denoise: bool = False, deskew: bool = False) -> np.ndarray:
    """
    Applies image enhancement operations for scanned documents.
    """
    if img is None:
        return img

    processed = img.copy()

    # Denoising
    if denoise:
        processed = cv2.fastNlMeansDenoisingColored(processed, None, 10, 10, 7, 21)

    # Convert to Grayscale
    gray = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)

    # Deskew if requested
    if deskew:
        coords = np.column_stack(np.where(gray > 0))
        if len(coords) > 0:
            angle = cv2.minAreaRect(coords)[-1]
            if angle < -45:
                angle = -(90 + angle)
            else:
                angle = -angle
            (h, w) = gray.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            gray = cv2.warpAffine(gray, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return gray
