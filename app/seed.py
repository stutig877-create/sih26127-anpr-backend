from datetime import datetime

from app.database.connection import SessionLocal, init_db
from app.models.blacklist import Blacklist
from app.models.camera import Camera
from app.models.detection import Detection
from app.services.detection_service import DetectionService


CAMERAS = [
    ("CAM001", "Main Gate", "Sector 1", 30.7333, 76.7794),
    ("CAM002", "North Gate", "Sector 2", 30.7500, 76.7900),
    ("CAM003", "Market Road", "Sector 3", 30.7400, 76.8000),
    ("CAM004", "Airport Road", "Sector 4", 30.7200, 76.8100),
]

SAMPLE_DETECTIONS = [
    ("PB10AB1234", "CAM001", datetime(2026, 9, 10, 10, 0), 94.5, "car"),
    ("PB10AB1234", "CAM002", datetime(2026, 9, 10, 10, 12), 95.0, "car"),
    ("PB08CD5678", "CAM003", datetime(2026, 9, 10, 10, 5), 91.0, "truck"),
    ("PB08CD5678", "CAM004", datetime(2026, 9, 10, 10, 20), 92.0, "truck"),
    ("CH01EF1234", "CAM001", datetime(2026, 9, 10, 10, 8), 89.5, "motorcycle"),
]


def seed_data() -> dict[str, int]:
    init_db()
    db = SessionLocal()
    try:
        cameras_added = 0
        for camera_id, name, location, latitude, longitude in CAMERAS:
            camera = db.query(Camera).filter(Camera.camera_id == camera_id).first()
            if camera is None:
                db.add(
                    Camera(
                        camera_id=camera_id,
                        name=name,
                        location=location,
                        latitude=latitude,
                        longitude=longitude,
                    )
                )
                cameras_added += 1
        db.commit()

        blacklist = db.query(Blacklist).filter(
            Blacklist.plate_number == "PB10AB1234"
        ).first()
        if blacklist is None:
            db.add(
                Blacklist(
                    plate_number="PB10AB1234",
                    reason="Sample blacklisted vehicle",
                    created_by="seed",
                )
            )
            db.commit()

        detections_added = 0
        service = DetectionService(db)
        for plate_number, camera_id, timestamp, confidence, vehicle_type in SAMPLE_DETECTIONS:
            existing = db.query(Detection).filter(
                Detection.plate_number == plate_number,
                Detection.camera_id == camera_id,
                Detection.timestamp == timestamp,
            ).first()
            if existing is not None:
                continue

            camera = db.query(Camera).filter(Camera.camera_id == camera_id).one()
            service.receive_detection(
                plate_number=plate_number,
                camera=camera,
                timestamp=timestamp,
                confidence=confidence,
                vehicle_type=vehicle_type,
            )
            detections_added += 1

        return {
            "cameras_added": cameras_added,
            "detections_added": detections_added,
            "vehicles_created": db.query(Detection.plate_number).distinct().count(),
            "blacklisted_plates": db.query(Blacklist).count(),
        }
    finally:
        db.close()


if __name__ == "__main__":
    print(seed_data())