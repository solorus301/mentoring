from fastapi import APIRouter, status
from app.schemas.category import CategoryCreateSchema, CategorySchema, CategoryUpdateSchema

category_router = APIRouter(prefix="/categories")

@category_router.get("", status_code=status.HTTP_200_OK)
def read_categories() -> list[CategorySchema]:
    ...

@category_router.post("", status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreateSchema, ) -> CategorySchema:
    ...

@category_router.patch("/{category_id}", status_code=status.HTTP_200_OK)
def update_category(category_id: str, payload: CategoryUpdateSchema, ) -> CategorySchema:
    ...

@category_router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, ):
    ...