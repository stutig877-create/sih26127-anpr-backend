"""Compatibility re-export package for app.models.

The canonical ORM definitions remain in app.database.models to preserve
existing database metadata and table behavior. These files make the
requested app.models folder structure available without changing routes,
services, or database tables.
"""

from app.database.models import (
    Alert,
    Base,
    Blacklist,
    Camera,
    Detection,
    Trajectory,
    UploadFileRecord,
    User,
    Vehicle,
)

__all__ = [
    "Alert",
    "Base",
    "Blacklist",
    "Camera",
    "Detection",
    "Trajectory",
    "UploadFileRecord",
    "User",
    "Vehicle",
]
