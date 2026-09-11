import asyncio

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.models import Base, Camera
from app.routes.alerts import list_active_alerts, list_alerts
from app.routes.analytics import get_camera_traffic, get_vehicle_count
from app.routes.blacklists import create_blacklist
from app.routes.detections import create_detection
from app.schemas.blacklist import BlacklistCreate
from app.schemas.detection import DetectionCreate
from datetime import datetime


@pytest.fixture
def db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)
        engine.dispose()


def add_camera(db, camera_id="CAM001"):
    camera = Camera(
        camera_id=camera_id,
        name=f"{camera_id} Gate",
        location="Sector 1",
        latitude=30.7333,
        longitude=76.7794,
    )
    db.add(camera)
    db.commit()
    return camera


def test_blacklist_alert_and_analytics(db):
    add_camera(db, "CAM001")
    add_camera(db, "CAM002")

    create_blacklist(BlacklistCreate(plate_number="PB10AB1234", reason="Wanted"), db)
    asyncio.run(create_detection(DetectionCreate(
        plate_number="PB10AB1234",
        camera_id="CAM001",
        timestamp=datetime(2026, 9, 10, 10, 30),
        confidence=94.5,
        vehicle_type="car",
    ), db))

    alerts = list_alerts(db)
    active = list_active_alerts(db)
    assert len(alerts) == 1
    assert len(active) == 1
    assert alerts[0]["plate"] == "PB10AB1234"

    asyncio.run(create_detection(DetectionCreate(
        plate_number="PB08CD5678",
        camera_id="CAM001",
        timestamp=datetime(2026, 9, 10, 10, 31),
        confidence=89.0,
        vehicle_type="car",
    ), db))
    asyncio.run(create_detection(DetectionCreate(
        plate_number="PB08CD5678",
        camera_id="CAM002",
        timestamp=datetime(2026, 9, 10, 10, 32),
        confidence=88.0,
        vehicle_type="car",
    ), db))

    assert get_vehicle_count(db) == {"vehicle_count": 2, "detection_count": 3}
    camera_counts = {item["camera_id"]: item["detection_count"] for item in get_camera_traffic(db)["cameras"]}
    assert camera_counts == {"CAM001": 2, "CAM002": 1}
