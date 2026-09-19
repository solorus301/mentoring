from fastapi import APIRouter, Depends, status

from app.schemas.category import CategoryCreateSchema, CategorySchema, CategoryUpdateSchema

from app.services.category import CategoriesService
from app.api.dependencies import get_category_service

category_router = APIRouter(prefix="/categories")

@category_router.get("", status_code=status.HTTP_200_OK)
def read_categories(category_service: CategoriesService = Depends(get_category_service)) -> list[CategorySchema]:
        return category_service.list_categories()

@category_router.post("", status_code=status.HTTP_201_CREATED)
def create_category(category_create: CategoryCreateSchema, category_service: CategoriesService = Depends(get_category_service)) -> CategorySchema:
    return category_service.create_category(category_create=category_create)

@category_router.patch("/{category_id}", status_code=status.HTTP_200_OK)
def update_category(category_id: str, payload: CategoryUpdateSchema, category_service: CategoriesService = Depends(get_category_service)) -> CategorySchema:
    return category_service.update_category(category_id=category_id, category_update=payload)

@category_router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, category_service: CategoriesService = Depends(get_category_service)) -> None:
        return category_service.delete_category(category_id=category_id)