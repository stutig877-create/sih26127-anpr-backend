from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class DetectionCreate(BaseModel):
    plate_number: str = Field(..., min_length=3, max_length=50)
    camera_id: str = Field(..., min_length=3, max_length=50, pattern=r"^[A-Za-z0-9][A-Za-z0-9_-]*$")
    timestamp: datetime
    confidence: float = Field(..., ge=0, le=100)
    vehicle_type: str = Field(..., min_length=2, max_length=50)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    location: Optional[str] = Field(None, max_length=255)

    @field_validator("plate_number")
    @classmethod
    def normalize_plate_number(cls, value: str) -> str:
        normalized = value.strip().upper()
        if not normalized.replace(" ", "").replace("-", "").isalnum():
            raise ValueError("plate number may contain only letters, numbers, spaces, and hyphens")
        return normalized


class DetectionUpdate(BaseModel):
    vehicle_id: Optional[int] = None
    camera_id: Optional[str] = Field(None, min_length=2, max_length=50)
    plate_number: Optional[str] = Field(None, min_length=2, max_length=50)
    timestamp: Optional[datetime] = None
    confidence: Optional[float] = Field(None, ge=0, le=100)
    vehicle_type: Optional[str] = Field(None, max_length=50)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    image_path: Optional[str] = Field(None, min_length=1, max_length=255)
    location: Optional[str] = Field(None, max_length=255)


class DetectionResponse(BaseModel):
    id: int
    vehicle_id: int
    camera_id: Optional[str] = None
    plate_number: Optional[str] = None
    timestamp: Optional[datetime] = None
    confidence: float
    vehicle_type: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    image_path: Optional[str] = None
    location: Optional[str] = None

    class Config:
        from_attributes = True
