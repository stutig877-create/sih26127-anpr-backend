from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.connection import init_db
from app.routes.upload import router as upload_router
from app.routes.anpr import router as anpr_router
from app.routes.vehicles import router as vehicle_router
from app.routes.detections import router as detection_router
from app.routes.analytics import router as analytics_router
from app.routes.cameras import router as camera_router
from app.routes.trajectories import router as trajectory_router
from app.routes.blacklists import router as blacklist_router
from app.routes.alerts import router as alert_router
from app.routes.auth import router as auth_router
from app.routes.websocket import router as websocket_router

@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="SIH26127 Backend",
    version="0.1.0",
    description="City-Wide AI Engine for Multi-Camera ANPR Trajectory Tracking and Urban Traffic Analytics - Person 1 Backend",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(anpr_router)
app.include_router(vehicle_router)
app.include_router(detection_router)
app.include_router(analytics_router)
app.include_router(camera_router)
app.include_router(trajectory_router)
app.include_router(blacklist_router)
app.include_router(alert_router)
app.include_router(auth_router)
app.include_router(websocket_router)


@app.get("/", tags=["Health"])
def read_root():
    return {
        "message": "SIH26127 backend is running",
        "phase": "PHASE 13",
        "status": "backend_ready",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
