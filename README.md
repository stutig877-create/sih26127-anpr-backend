# SIH26127 Backend

FastAPI backend for the SIH26127 city-wide multi-camera ANPR tracking and traffic
analytics system. The backend receives detection data from the separate AI service;
it does not run OCR or vehicle-detection models.

## Run locally

```powershell
cd c:\Users\hplap\OneDrive\Documents\SIH26127\backend
.\.venv\Scripts\python.exe -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Copy `.env.example` to `.env` and set `DATABASE_URL` before starting the server.

## API docs

- Swagger: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Run tests

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
```

## Seed demo data

With the project virtual environment active, run:

```powershell
python -m app.seed
```

This creates four cameras, three sample vehicles with detections and trajectories,
and a blacklisted vehicle that generates an alert automatically. The command is safe
to run more than once.
