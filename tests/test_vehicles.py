import asyncio

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.models import Base, Camera
from app.routes.vehicles import create_vehicle, get_vehicle, get_vehicle_history
from app.schemas.vehicle import VehicleCreate
from app.routes.detections import create_detection
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


def detection_payload(plate="PB10AB1234", camera_id="CAM001", minute=30):
    return DetectionCreate(
        plate_number=plate,
        camera_id=camera_id,
        timestamp=datetime(2026, 9, 10, 10, minute),
        confidence=94.5,
        vehicle_type="car",
    )


def test_vehicle_create_get_history(db):
    add_camera(db)

    created = create_vehicle(
        VehicleCreate(
            plate_number="PB10AB1234",
            camera_id="CAM001",
            timestamp=datetime(2026, 9, 10, 10, 30),
            location="Sector 1",
        ),
        db,
    )
    assert created.plate_number == "PB10AB1234"

    vehicle = get_vehicle("pb10ab1234", db)
    assert vehicle.plate_number == "PB10AB1234"

    asyncio.run(create_detection(detection_payload(minute=31), db))
    history = get_vehicle_history("PB10AB1234", db)
    assert len(history) >= 1
    assert history[0]["camera"] == "CAM001"
