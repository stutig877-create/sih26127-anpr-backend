from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.upload import router as upload_router
from app.routes.anpr import router as anpr_router
from app.routes.vehicles import router as vehicle_router
from app.routes.detections import router as detection_router
from app.routes.analytics import router as analytics_router
from app.database.connection import engine
from app.database.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SIH26127 Backend",
    version="0.1.0",
    description="City-Wide AI Engine for Multi-Camera ANPR Trajectory Tracking and Urban Traffic Analytics - Person 1 Backend",
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


@app.get("/", tags=["Health"])
def read_root():
    return {
        "message": "SIH26127 backend is running",
        "phase": "PHASE 1",
        "status": "basic_fastapi_server",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
