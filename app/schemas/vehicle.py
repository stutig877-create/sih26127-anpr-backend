from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class VehicleCreate(BaseModel):
    plate_number: str = Field(..., min_length=3, max_length=50, description="Vehicle plate number")
    camera_id: str = Field(..., min_length=2, max_length=50, description="Camera identifier")
    timestamp: datetime = Field(..., description="Detection time")
    location: Optional[str] = Field(None, max_length=255)


class VehicleResponse(BaseModel):
    id: int
    plate_number: str
    camera_id: str
    timestamp: datetime
    location: Optional[str] = None

    class Config:
        from_attributes = True


class DetectionCreate(BaseModel):
    vehicle_id: int
    image_path: str
    confidence: float = Field(..., ge=0, le=100)
