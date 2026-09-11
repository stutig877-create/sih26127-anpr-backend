from collections import Counter, defaultdict

from sqlalchemy.orm import Session

from app.models.detection import Detection


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def detections(self):
        return self.db.query(Detection).order_by(
            Detection.timestamp, Detection.id
        ).all()

    def vehicle_count(self):
        detections = self.detections()
        return {
            "vehicle_count": len({detection.plate_number for detection in detections}),
            "detection_count": len(detections),
        }

    def camera_traffic(self):
        detections = self.detections()
        counts = Counter(detection.camera_id for detection in detections)
        vehicles = defaultdict(set)
        for detection in detections:
            vehicles[detection.camera_id].add(detection.plate_number)

        return [
            {
                "camera_id": camera_id,
                "detection_count": counts[camera_id],
                "vehicle_count": len(vehicles[camera_id]),
            }
            for camera_id in sorted(counts)
        ]

    def congestion(self):
        detection_count = len(self.detections())
        if detection_count <= 10:
            level = "LOW"
        elif detection_count <= 30:
            level = "MEDIUM"
        else:
            level = "HIGH"

        return {
            "level": level,
            "detection_count": detection_count,
            "thresholds": {"low_max": 10, "medium_max": 30},
        }

    def origin_destination(self):
        detections = self.detections()
        by_vehicle = defaultdict(list)
        for detection in detections:
            by_vehicle[detection.plate_number].append(detection)

        route_counts = Counter()
        for vehicle_detections in by_vehicle.values():
            origin = vehicle_detections[0].camera_id
            destination = vehicle_detections[-1].camera_id
            route_counts[(origin, destination)] += 1

        return [
            {
                "origin_camera": origin,
                "destination_camera": destination,
                "vehicle_count": count,
            }
            for (origin, destination), count in sorted(route_counts.items())
        ]