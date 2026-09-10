from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.models import Detection, Vehicle
from app.schemas.detection import DetectionCreate, DetectionResponse
from app.services.vehicle_service import VehicleService

router = APIRouter(tags=["Detections"])


@router.post("/track-vehicle", response_model=DetectionResponse, status_code=status.HTTP_201_CREATED)
@router.post("/detections", response_model=DetectionResponse, status_code=status.HTTP_201_CREATED)
def create_detection(payload: DetectionCreate, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == payload.vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    if payload.confidence < 0 or payload.confidence > 100:
        raise HTTPException(status_code=400, detail="Invalid confidence")

    service = VehicleService(db)
    detection = service.add_detection(payload.vehicle_id, payload.image_path, payload.confidence)
    return detection
