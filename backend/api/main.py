# backend\api\main.py
print("🔥 RUNNING backend/main.py 🔥")

from fastapi import APIRouter
from .routes import tasks

api_router = APIRouter()

# Include all route modules
api_router.include_router(tasks.router, prefix="/api", tags=["tasks"])