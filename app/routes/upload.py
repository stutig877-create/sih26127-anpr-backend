from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.utils.file_utils import save_upload_file
from app.schemas.upload import UploadImageResponse

router = APIRouter(tags=["Upload"])


@router.post("/upload-image", response_model=UploadImageResponse, summary="Upload image file", description="Upload an image file to the server uploads folder.")
@router.post("/upload/image", response_model=UploadImageResponse, summary="Upload image file", description="Upload an image file to the server uploads folder.")
async def upload_image(file: UploadFile = File(...)):
    allowed_types = {"image/jpeg", "image/png", "image/jpg"}
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid image type. Only JPG, JPEG, and PNG are allowed.")

    metadata = save_upload_file(file, upload_dir="uploads")
    return UploadImageResponse(**metadata)
