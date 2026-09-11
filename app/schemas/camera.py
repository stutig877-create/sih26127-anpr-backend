from typing import Literal, Optional
from pydantic import BaseModel, Field


CameraStatus = Literal["active", "inactive", "offline"]


class CameraCreate(BaseModel):
    camera_id: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9_-]*$",
        description="Unique camera identifier",
    )
    name: str = Field(..., min_length=2, max_length=255, description="Camera label")
    location: str = Field(..., min_length=2, max_length=255, description="Area or landmark label")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate")
    status: CameraStatus = Field(default="active", description="Camera status")


class CameraUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    location: Optional[str] = Field(None, min_length=2, max_length=255)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    status: Optional[CameraStatus] = None


class CameraResponse(BaseModel):
    id: int
    camera_id: str
    name: str
    location: str
    latitude: float
    longitude: float
    status: str

    class Config:
        from_attributes = True
