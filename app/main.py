from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.database import init_db
from app.core.logging import configure_logging

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging()
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Local-first hybrid memory system for AI agents.",
    lifespan=lifespan,
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "message": "MemForge is running",
        "docs": "/docs",
        "health": "/health",
    }
