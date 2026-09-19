from fastapi import APIRouter

from app.api.routers.tasks import task_router
from app.api.routers.category import category_router


api_router = APIRouter()
api_router.include_router(task_router)
api_router.include_router(category_router)