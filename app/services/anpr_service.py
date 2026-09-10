from pathlib import Path


class PlateDetectionService:
    """Simple modular service layer for ANPR. Replace placeholder logic with YOLO + OCR later."""

    def detect_plate(self, image_path: str) -> dict:
        """Return a placeholder plate detection response.

        Later this method can call YOLO and OCR modules.
        """
        path = Path(image_path)
        return {
            "plate_text": "PB10AB1234",
            "confidence": 0.93,
            "image_path": str(path),
            "source": "placeholder",
        }


class OCRService:
    """OCR extraction service placeholder. Keep modular for EasyOCR plug-in later."""

    def extract_text(self, image_path: str) -> str:
        """Return plate text from an image. Placeholder implementation returns sample value."""
        return "PB10AB1234"


class ANPRService:
    """Main service that calls detection + OCR module in a clean order."""

    def __init__(self):
        self.detector = PlateDetectionService()
        self.ocr = OCRService()

    def process_image(self, image_path: str) -> dict:
        detection = self.detector.detect_plate(image_path)
        plate_text = self.ocr.extract_text(image_path)

        return {
            "plate_text": plate_text,
            "confidence": detection.get("confidence", 0.0),
            "image_path": detection.get("image_path", image_path),
            "source": "anpr_service",
        }
