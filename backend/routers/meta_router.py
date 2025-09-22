from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "blueprint_2_enabled": True
    }


@router.get("/")
async def root():
    return {
        "message": "Dubai Real Estate RAG Chat System API",
        "version": "1.2.0",
        "status": "running",
        "docs": "/docs"
    }

