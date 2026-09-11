from typing import Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class BlacklistCreate(BaseModel):
    plate_number: str = Field(..., min_length=2, max_length=50, description="Vehicle plate to blacklist")
    reason: Optional[str] = Field(None, min_length=2, max_length=500, description="Blacklist reason")
    created_by: Optional[str] = Field(None, max_length=255, description="Operator / system that created the entry")

    @field_validator("plate_number")
    @classmethod
    def normalize_plate_number(cls, value: str) -> str:
        normalized = value.strip().upper()
        if not normalized.replace(" ", "").replace("-", "").isalnum():
            raise ValueError("plate number may contain only letters, numbers, spaces, and hyphens")
        return normalized


class BlacklistUpdate(BaseModel):
    plate_number: Optional[str] = Field(None, min_length=2, max_length=50)
    reason: Optional[str] = Field(None, min_length=2, max_length=500)
    created_by: Optional[str] = Field(None, max_length=255)

    @field_validator("plate_number")
    @classmethod
    def normalize_plate_number(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip().upper()
        if not normalized.replace(" ", "").replace("-", "").isalnum():
            raise ValueError("plate number may contain only letters, numbers, spaces, and hyphens")
        return normalized


class BlacklistResponse(BaseModel):
    id: int
    plate_number: str
    reason: Optional[str] = None
    created_at: Optional[datetime] = None
    created_by: Optional[str] = None

    class Config:
        from_attributes = True
