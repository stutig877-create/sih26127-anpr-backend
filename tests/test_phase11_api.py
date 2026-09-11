import asyncio
from datetime import datetime

import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.models import Base, Camera, User
from app.routes.alerts import list_active_alerts, list_alerts, update_alert
from app.routes.analytics import (
    get_camera_traffic,
    get_congestion,
    get_origin_destination,
    get_vehicle_count,
)
from app.routes.auth import login, register
from app.routes.blacklists import (
    create_blacklist,
    delete_blacklist_by_plate,
    get_blacklist_by_plate,
)
from app.routes.cameras import (
    create_camera,
    delete_camera,
    get_camera,
    list_cameras,
    update_camera,
)
from app.routes.detections import create_detection
from app.routes.trajectories import get_vehicle_trajectory
from app.routes.vehicles import get_vehicle, get_vehicle_history
from app.schemas.alert import AlertUpdate
from app.schemas.auth import LoginRequest, RegisterRequest
from app.schemas.blacklist import BlacklistCreate
from app.schemas.camera import CameraCreate, CameraUpdate
from app.schemas.detection import DetectionCreate
from app.schemas.trajectory import VehicleTrajectoryResponse


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


def test_register_and_login(db):
    user = register(
        RegisterRequest(
            email="operator@example.com",
            password="StrongPass123",
            full_name="Test Operator",
            role="operator",
        ),
        db,
    )
    stored = db.query(User).filter(User.id == user.id).one()
    assert stored.password_hash != "StrongPass123"

    token = login(LoginRequest(email="operator@example.com", password="StrongPass123"), db)
    assert token["token_type"] == "bearer"
    assert token["user"].role == "operator"


def test_camera_crud(db):
    payload = CameraCreate(
        camera_id="CAM001",
        name="Main Gate",
        location="Sector 1",
        latitude=30.7333,
        longitude=76.7794,
    )
    created = create_camera(payload, db)
    assert created.camera_id == "CAM001"
    assert len(list_cameras(db)) == 1
    assert get_camera("CAM001", db).name == "Main Gate"

    updated = update_camera("CAM001", CameraUpdate(status="inactive"), db)
    assert updated.status == "inactive"

    delete_camera("CAM001", db)
    with pytest.raises(HTTPException) as error:
        get_camera("CAM001", db)
    assert error.value.status_code == 404


def test_detection_creation_and_vehicle_retrieval(db):
    add_camera(db)
    detection = asyncio.run(create_detection(detection_payload(), db))
    vehicle = get_vehicle("pb10ab1234", db)

    assert detection.plate_number == "PB10AB1234"
    assert vehicle.plate_number == "PB10AB1234"
    assert vehicle.last_seen == datetime(2026, 9, 10, 10, 30)


def test_vehicle_history_and_trajectory(db):
    add_camera(db)
    asyncio.run(create_detection(detection_payload(minute=30), db))
    asyncio.run(create_detection(detection_payload(minute=35), db))

    history = get_vehicle_history("PB10AB1234", db)
    trajectory = VehicleTrajectoryResponse.model_validate(
        get_vehicle_trajectory("PB10AB1234", db)
    )
    assert len(history) == 2
    assert history[0]["camera"] == "CAM001"
    assert [point.sequence for point in trajectory.points] == [1, 2]


def test_blacklist_and_automatic_alert_creation(db):
    add_camera(db)
    create_blacklist(BlacklistCreate(plate_number="pb10ab1234", reason="Wanted"), db)
    asyncio.run(create_detection(detection_payload(), db))

    alerts = list_alerts(db)
    assert len(alerts) == 1
    assert alerts[0]["plate"] == "PB10AB1234"
    assert len(list_active_alerts(db)) == 1

    update_alert(alerts[0]["id"], AlertUpdate(status="resolved"), db)
    assert list_active_alerts(db) == []
    assert get_blacklist_by_plate("PB10AB1234", db).plate_number == "PB10AB1234"
    delete_blacklist_by_plate("PB10AB1234", db)


def test_analytics(db):
    add_camera(db, "CAM001")
    add_camera(db, "CAM002")
    asyncio.run(create_detection(detection_payload(camera_id="CAM001", minute=1), db))
    asyncio.run(create_detection(detection_payload(camera_id="CAM002", minute=2), db))
    asyncio.run(
        create_detection(
            detection_payload(plate="PB08CD5678", camera_id="CAM001", minute=3),
            db,
        )
    )

    assert get_vehicle_count(db) == {"vehicle_count": 2, "detection_count": 3}
    camera_counts = {item["camera_id"]: item["detection_count"] for item in get_camera_traffic(db)["cameras"]}
    assert camera_counts == {"CAM001": 2, "CAM002": 1}
    assert get_congestion(db)["level"] == "LOW"
    routes = get_origin_destination(db)["routes"]
    assert any(
        route["origin_camera"] == "CAM001"
        and route["destination_camera"] == "CAM002"
        for route in routes
    )