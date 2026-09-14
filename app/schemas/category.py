from pydantic import BaseModel, ConfigDict

class CategorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    completed: bool = False

class CategoryCreateSchema(BaseModel):
    name: str

class CategoryUpdateSchema(BaseModel):
    name: str | None = None
    completed: bool | None = None