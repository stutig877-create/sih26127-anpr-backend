from sqlalchemy.orm import Session
from app.database.models import Vehicle, Detection


class VehicleService:
    def __init__(self, db: Session):
        self.db = db

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

    def get_vehicle_by_plate(self, plate_number: str) -> Vehicle | None:
        return self.db.query(Vehicle).filter(Vehicle.plate_number == plate_number).first()

    def add_detection(self, vehicle_id: int, image_path: str, confidence: float) -> Detection:
        detection = Detection(vehicle_id=vehicle_id, image_path=image_path, confidence=confidence)
        self.db.add(detection)
        self.db.commit()
        self.db.refresh(detection)
        return detection
