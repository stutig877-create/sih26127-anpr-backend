from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class VehicleCreate(BaseModel):
    plate_number: str = Field(..., min_length=3, max_length=50, description="Vehicle plate number")
    camera_id: str = Field(..., min_length=2, max_length=50, description="Camera identifier")
    timestamp: datetime = Field(..., description="Detection time")
    location: Optional[str] = Field(None, max_length=255)

    @field_validator("plate_number")
    @classmethod
    def normalize_plate_number(cls, value: str) -> str:
        normalized = value.strip().upper()
        if not normalized.replace(" ", "").replace("-", "").isalnum():
            raise ValueError("plate number may contain only letters, numbers, spaces, and hyphens")
        return normalized


class VehicleUpdate(BaseModel):
    plate_number: Optional[str] = Field(None, min_length=3, max_length=50)
    camera_id: Optional[str] = Field(None, min_length=2, max_length=50)
    timestamp: Optional[datetime] = None
    location: Optional[str] = Field(None, max_length=255)

    @field_validator("plate_number")
    @classmethod
    def normalize_plate_number(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip().upper()
        if not normalized.replace(" ", "").replace("-", "").isalnum():
            raise ValueError("plate number may contain only letters, numbers, spaces, and hyphens")
        return normalized


class VehicleResponse(BaseModel):
    id: int
    plate_number: str
    camera_id: str
    timestamp: datetime
    location: Optional[str] = None

    class Config:
        from_attributes = True


class VehicleHistoryResponse(BaseModel):
    plate: str
    camera: str
    timestamp: datetime
    location: str | None = None
    confidence: float
    vehicle_type: str | None = None
