from pydantic import BaseModel, Field
from typing import Optional


class UploadImageResponse(BaseModel):
    filename: str
    stored_filename: str
    file_path: str
    size: int
    content_type: Optional[str] = None
