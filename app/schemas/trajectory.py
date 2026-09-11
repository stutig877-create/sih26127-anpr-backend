from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class TrajectoryCreate(BaseModel):
    vehicle_id: int = Field(..., description="Related vehicle id")
    camera_id: str = Field(..., min_length=2, max_length=50, description="Camera id")
    timestamp: Optional[datetime] = Field(default=None, description="Observation timestamp")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate")
    sequence: int = Field(default=1, ge=1, description="Route sequence number")


class TrajectoryUpdate(BaseModel):
    vehicle_id: Optional[int] = None
    camera_id: Optional[str] = Field(None, min_length=2, max_length=50)
    timestamp: Optional[datetime] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    sequence: Optional[int] = Field(None, ge=1)


class TrajectoryResponse(BaseModel):
    id: int
    vehicle_id: int
    camera_id: str
    timestamp: Optional[datetime] = None
    latitude: float
    longitude: float
    sequence: int

    class Config:
        from_attributes = True


class TrajectoryPointResponse(BaseModel):
    camera_id: str
    timestamp: datetime
    latitude: float
    longitude: float
    sequence: int


class VehicleTrajectoryResponse(BaseModel):
    plate_number: str
    vehicle_id: int
    points: list[TrajectoryPointResponse]
