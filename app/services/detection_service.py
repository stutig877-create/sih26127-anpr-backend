from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.blacklist import Blacklist
from app.models.camera import Camera
from app.models.detection import Detection
from app.models.trajectory import Trajectory
from app.models.vehicle import Vehicle


class DetectionService:
    def __init__(self, db: Session):
        self.db = db

    def list_detections(self):
        return self.db.query(Detection).order_by(Detection.id).all()

    def get_detection(self, detection_id: int):
        return self.db.query(Detection).filter(Detection.id == detection_id).first()

    def receive_detection(self, *, plate_number: str, camera: Camera, timestamp: datetime,
                          confidence: float, vehicle_type: str, latitude: float | None = None,
                          longitude: float | None = None, location: str | None = None):
        vehicle = self.db.query(Vehicle).filter(Vehicle.plate_number == plate_number).first()
        observation_location = location or camera.location
        observation_latitude = latitude if latitude is not None else camera.latitude
        observation_longitude = longitude if longitude is not None else camera.longitude

        if vehicle is None:
            vehicle = Vehicle(
                plate_number=plate_number,
                camera_id=camera.camera_id,
                vehicle_type=vehicle_type,
                timestamp=timestamp,
                first_seen=timestamp,
                last_seen=timestamp,
                location=observation_location,
                confidence=confidence,
            )
            self.db.add(vehicle)
            self.db.flush()
        else:
            vehicle.camera_id = camera.camera_id
            vehicle.vehicle_type = vehicle_type
            vehicle.timestamp = timestamp
            vehicle.first_seen = min(vehicle.first_seen or timestamp, timestamp)
            vehicle.last_seen = max(vehicle.last_seen or timestamp, timestamp)
            vehicle.location = observation_location
            vehicle.confidence = confidence

        detection = Detection(
            vehicle_id=vehicle.id,
            camera_id=camera.camera_id,
            plate_number=plate_number,
            timestamp=timestamp,
            confidence=confidence,
            vehicle_type=vehicle_type,
            latitude=observation_latitude,
            longitude=observation_longitude,
            location=observation_location,
        )
        self.db.add(detection)
        self.db.flush()

        next_sequence = self.db.query(func.max(Trajectory.sequence)).filter(
            Trajectory.vehicle_id == vehicle.id
        ).scalar() or 0
        trajectory = Trajectory(
            vehicle_id=vehicle.id,
            camera_id=camera.camera_id,
            timestamp=timestamp,
            latitude=observation_latitude,
            longitude=observation_longitude,
            sequence=next_sequence + 1,
        )
        self.db.add(trajectory)

        blacklist = self.db.query(Blacklist).filter(
            Blacklist.plate_number == plate_number
        ).first()
        alert = None
        if blacklist:
            alert = Alert(
                vehicle_id=vehicle.id,
                plate_number=plate_number,
                camera_id=camera.camera_id,
                detection_id=detection.id,
                timestamp=timestamp,
                alert_type="blacklist",
                severity="high",
                message=blacklist.reason or f"Blacklisted vehicle detected: {plate_number}",
                status="active",
            )
            self.db.add(alert)

        self.db.commit()
        self.db.refresh(detection)
        if alert:
            self.db.refresh(alert)
        return detection, alert

    def update_detection(self, detection: Detection, **kwargs):
        for field, value in kwargs.items():
            if value is not None:
                setattr(detection, field, value)
        self.db.commit()
        self.db.refresh(detection)
        return detection

    def delete_detection(self, detection: Detection):
        self.db.delete(detection)
        self.db.commit()
        return True
