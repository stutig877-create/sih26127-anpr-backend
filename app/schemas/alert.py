from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AlertResponse(BaseModel):
    id: int
    vehicle: Optional[int] = None
    plate: str
    camera: str
    timestamp: datetime
    alert_type: str
    severity: str
    message: str
    status: str


class AlertUpdate(BaseModel):
    status: Optional[str] = Field(None, min_length=2, max_length=50)
    severity: Optional[str] = Field(None, min_length=2, max_length=50)
    message: Optional[str] = Field(None, min_length=2, max_length=500)