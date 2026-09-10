from fastapi import APIRouter, HTTPException, UploadFile, File
from app.services.anpr_service import ANPRService

router = APIRouter(tags=["ANPR"])
service = ANPRService()


@router.post("/detect-plate", summary="Detect and extract plate text", description="Detect a plate from a received image and return extracted plate text.")
@router.post("/anpr/detect-plate", summary="Detect and extract plate text", description="Detect a plate from a received image and return extracted plate text.")
def detect_plate(file: UploadFile = File(...)):
    allowed_types = {"image/jpeg", "image/png", "image/jpg"}
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid image type. Only JPG, JPEG, and PNG are allowed.")

    image_path = f"uploads/{file.filename}"
    result = service.process_image(image_path)
    return result
