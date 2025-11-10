from fastapi import FastAPI
from app.config import settings
from app.api.routes import api_router

app = FastAPI(
    title="FastAPI Cloud Project",
    description="Проект с полным стеком технологий для GitLab CI",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "FastAPI Cloud Project", 
        "version": "1.0.0",
        "environment": settings.environment
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}