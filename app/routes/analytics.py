from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.models import Detection, Vehicle

router = APIRouter(tags=["Analytics"])


@router.get("/analytics", summary="Return dashboard analytics", description="Return simple analytics counts from detections and vehicles.")
def get_analytics(db: Session = Depends(get_db)):
    vehicle_count = db.query(Vehicle).count()
    detection_count = db.query(Detection).count()

    return {
        "vehicle_count": vehicle_count,
        "detection_count": detection_count,
        "message": "Simple analytics endpoint",
    }
