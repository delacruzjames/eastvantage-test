from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.models import Address  # noqa: F401
from app.routers import addresses, health

app = FastAPI(
    title=settings.app_name,
    description="REST API built with FastAPI and SQLite. Interactive docs are available at /docs.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(addresses.router, prefix="/addresses", tags=["Addresses"])
