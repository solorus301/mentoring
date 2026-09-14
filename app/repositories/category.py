from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import CategoryORM


class CategoryRepository:
    def __init__(self, db: Session) -> None:
            self.db = db

    def get_all(self) -> list(CategoryORM):
        return self.db.scalars(select(TaskORM)).all()

    def get_by_id(self, category_id: str) -> CategoryORM:
        return self.db.get(CategoryORM, category_id)

    def create(self, name: str) -> CategoryORM:
        new_categories = CategoryORM(name)
        self.db.add(new_categories)
        return new_categories

    def delete(self, CategoryORM) -> None:
        self.db.delete(CategoryORM)