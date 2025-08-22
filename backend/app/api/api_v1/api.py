from fastapi import APIRouter
from app.api.api_v1.endpoints import interviews, tasks

api_router = APIRouter()
api_router.include_router(interviews.router, prefix="/interviews", tags=["interviews"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
