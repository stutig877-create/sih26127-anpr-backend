from pydantic import BaseModel, Field
from typing import Optional


class DetectionCreate(BaseModel):
    vehicle_id: int
    image_path: str = Field(..., min_length=1, description="Stored image path")
    confidence: float = Field(..., ge=0, le=100)


class DetectionResponse(BaseModel):
    id: int
    vehicle_id: int
    image_path: str
    confidence: float

    class Config:
        from_attributes = True
