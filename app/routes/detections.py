from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.camera import Camera
from app.models.detection import Detection
from app.schemas.detection import DetectionCreate, DetectionResponse, DetectionUpdate
from app.services.detection_service import DetectionService
from app.services.live_updates import live_updates

router = APIRouter(tags=["Detections"])


@router.post("/track-vehicle", response_model=DetectionResponse, status_code=status.HTTP_201_CREATED)
@router.post("/detections", response_model=DetectionResponse, status_code=status.HTTP_201_CREATED)
async def create_detection(payload: DetectionCreate, db: Session = Depends(get_db)):
    camera = db.query(Camera).filter(Camera.camera_id == payload.camera_id).first()
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")

    service = DetectionService(db)
    detection, alert = service.receive_detection(
        plate_number=payload.plate_number,
        camera=camera,
        timestamp=payload.timestamp,
        confidence=payload.confidence,
        vehicle_type=payload.vehicle_type,
        latitude=payload.latitude,
        longitude=payload.longitude,
        location=payload.location,
    )
    await live_updates.broadcast({
        "type": "alert" if alert else "detection",
        "detection_id": detection.id,
        "plate_number": detection.plate_number,
        "camera_id": detection.camera_id,
        "alert_id": alert.id if alert else None,
    })
    return detection


@router.get("/detections", response_model=list[DetectionResponse])
def list_detections(db: Session = Depends(get_db)):
    service = DetectionService(db)
    return service.list_detections()


@router.get("/detections/{detection_id}", response_model=DetectionResponse)
def get_detection(detection_id: int, db: Session = Depends(get_db)):
    service = DetectionService(db)
    detection = service.get_detection(detection_id)
    if not detection:
        raise HTTPException(status_code=404, detail="Detection not found")
    return detection


@router.put("/detections/{detection_id}", response_model=DetectionResponse)
def update_detection(detection_id: int, payload: DetectionUpdate, db: Session = Depends(get_db)):
    service = DetectionService(db)
    detection = service.get_detection(detection_id)
    if not detection:
        raise HTTPException(status_code=404, detail="Detection not found")

    if payload.confidence is not None and (payload.confidence < 0 or payload.confidence > 100):
        raise HTTPException(status_code=400, detail="Invalid confidence")

    if payload.latitude is not None and (payload.latitude < -90 or payload.latitude > 90):
        raise HTTPException(status_code=400, detail="Latitude must be between -90 and 90")

    if payload.longitude is not None and (payload.longitude < -180 or payload.longitude > 180):
        raise HTTPException(status_code=400, detail="Longitude must be between -180 and 180")

    updated = service.update_detection(
        detection,
        vehicle_id=payload.vehicle_id,
        camera_id=payload.camera_id,
        plate_number=payload.plate_number,
        timestamp=payload.timestamp,
        confidence=payload.confidence,
        vehicle_type=payload.vehicle_type,
        latitude=payload.latitude,
        longitude=payload.longitude,
        image_path=payload.image_path,
        location=payload.location,
    )
    return updated


@router.delete("/detections/{detection_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_detection(detection_id: int, db: Session = Depends(get_db)):
    service = DetectionService(db)
    detection = service.get_detection(detection_id)
    if not detection:
        raise HTTPException(status_code=404, detail="Detection not found")

    service.delete_detection(detection)
