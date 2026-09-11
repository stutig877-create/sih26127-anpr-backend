from sqlalchemy.orm import Session
from app.models.vehicle import Vehicle
from app.models.detection import Detection


class VehicleService:
    def __init__(self, db: Session):
        self.db = db

    def list_vehicles(self):
        return self.db.query(Vehicle).order_by(Vehicle.id).all()

    def get_vehicle(self, vehicle_id: int):
        return self.db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    def get_vehicle_by_plate(self, plate_number: str) -> Vehicle | None:
        return self.db.query(Vehicle).filter(Vehicle.plate_number == plate_number).first()

    def get_history_by_plate(self, plate_number: str):
        vehicle = self.get_vehicle_by_plate(plate_number)
        if vehicle is None:
            return None

        return [
            {
                "plate": detection.plate_number,
                "camera": detection.camera_id,
                "timestamp": detection.timestamp,
                "location": detection.location or (
                    detection.camera.location if detection.camera else None
                ),
                "confidence": detection.confidence,
                "vehicle_type": detection.vehicle_type,
            }
            for detection in sorted(
                vehicle.detections,
                key=lambda item: (item.timestamp, item.id),
            )
        ]

    def create_vehicle(self, plate_number: str, camera_id: str, timestamp, location: str | None = None) -> Vehicle:
        vehicle = Vehicle(
            plate_number=plate_number,
            camera_id=camera_id,
            timestamp=timestamp,
            location=location,
        )
        self.db.add(vehicle)
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle

    def update_vehicle(self, vehicle: Vehicle, **kwargs):
        for field, value in kwargs.items():
            if value is not None:
                setattr(vehicle, field, value)
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle

    def delete_vehicle(self, vehicle: Vehicle):
        self.db.delete(vehicle)
        self.db.commit()
        return True

    def add_detection(self, vehicle_id: int, image_path: str, confidence: float) -> Detection:
        detection = Detection(vehicle_id=vehicle_id, image_path=image_path, confidence=confidence)
        self.db.add(detection)
        self.db.commit()
        self.db.refresh(detection)
        return detection
