from sqlalchemy.orm import Session
from app.repositories.category import CategoryRepository
from app.schemas.category import CategoryCreateSchema, CategorySchema, CategoryUpdateSchema



class CategoriesService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.category_repository = CategoryRepository(db)

    def list_categories(self) -> list[CategorySchema]:
        categories_orm = self.category_repository.get_all()
        return [CategorySchema.model_validate(category) for category in categories_orm]

    def create_category(self, category_create: CategoryCreateSchema) -> CategorySchema:
        category_orm = self.category_repository.create(name=category_create.name)
        self.db.commit()
        return CategorySchema.model_validate(category_orm)

    def update_task(self, category_id: str, category_update: CategoryUpdateSchema) -> CategorySchema:
        category_for_update = self.category_repository.get_by_id(category_id=category_id)
        if category_for_update.title is not None:
            category_for_update.title = category_for_update.title
        if category_for_update.completed is not None:
            category_for_update.completed = category_for_update.completed