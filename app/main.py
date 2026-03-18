from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.interview import router as interview_router

app = FastAPI(title="JobCompass AI - Interview Service")

app.include_router(health_router)
app.include_router(interview_router)