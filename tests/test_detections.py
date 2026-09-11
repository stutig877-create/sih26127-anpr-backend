import asyncio

import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.models import Base, Camera
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


def test_detection_create_invalid_confidence_and_missing_camera(db):
    add_camera(db)

    detection = asyncio.run(create_detection(DetectionCreate(
        plate_number="PB10AB1234",
        camera_id="CAM001",
        timestamp=datetime(2026, 9, 10, 10, 30),
        confidence=94.5,
        vehicle_type="car",
    ), db))
    assert detection.plate_number == "PB10AB1234"

    with pytest.raises(ValidationError):
        DetectionCreate(
            plate_number="PB10AB1234",
            camera_id="CAM001",
            timestamp=datetime(2026, 9, 10, 10, 31),
            confidence=101,
            vehicle_type="car",
        )

    with pytest.raises(HTTPException) as exc:
        asyncio.run(create_detection(DetectionCreate(
            plate_number="PB99ZZ9999",
            camera_id="NOPE",
            timestamp=datetime(2026, 9, 10, 10, 31),
            confidence=94.5,
            vehicle_type="car",
        ), db))
    assert exc.value.status_code == 404
