from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase, Mapped, mapped_column

DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:15432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))

class TaskORM(Base):
    __tablename__ = "tasks"

    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)

class CategoryORM(Base):
    __tablename__ = "categories"

    name: Mapped[str]


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool = False

class TaskCreateSchema(BaseModel):
    title: str

class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None

class CategorySchema(BaseModel):
    id: str
    name: str

class CategoryCreateSchema(BaseModel):
    name: str

class CategoryUpdateSchema(BaseModel):
    name: str | None = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def task_orm_to_model(task_orm: TaskORM) -> TaskSchema:
    return TaskSchema(id=task_orm.id, title=task_orm.title, completed=task_orm.completed)

def category_orm_to_model(category_orm: CategorySchema) -> CategorySchema:
    return CategorySchema(id=category_orm.id, name=category_orm.name)



@app.get("/tasks", status_code=status.HTTP_200_OK)
def read_tasks(db: Session = Depends(get_db)) -> list[TaskSchema]:
    tasks_from_db = db.scalars(select(TaskORM)).all()
    return [task_orm_to_model(task) for task in tasks_from_db]

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema, db: Session = Depends(get_db)) -> TaskSchema:
    new_task = TaskORM(title=payload.title, completed=False)

    db.add(new_task)
    db.commit()
    return task_orm_to_model(new_task)

@app.patch("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def update_task(task_id: str, payload: TaskUpdateSchema, db: Session = Depends(get_db)) -> TaskSchema:
    task_for_update = db.get(TaskORM, task_id)
    if task_for_update is not None:
        if payload.title is not None:
            task_for_update.title = payload.title
        if payload.completed is not None:
            task_for_update.completed = payload.completed

        db.commit()
        db.refresh(task_for_update)
        return task_orm_to_model(task_for_update)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session = Depends(get_db)) -> None:
    task_for_delete = db.get(TaskORM, task_id)
    db.delete(task_for_delete)
    db.commit()
    

@app.get("/categories", status_code=status.HTTP_200_OK)
def read_categories(db: Session = Depends(get_db)) -> list[CategorySchema]:
    categories_from_db = db.scalars(select(CategoryORM)).all()
    return [category_orm_to_model(category) for category in categories_from_db]

@app.post("/categories", status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreateSchema, db: Session = Depends(get_db)) -> CategorySchema:
    new_category = CategoryORM(name=payload.name)

    db.add(new_category)
    db.commit()
    return category_orm_to_model(new_category)

@app.patch("/categories/{category_id}", status_code=status.HTTP_200_OK)
def update_category(category_id: str, payload: CategoryUpdateSchema, db: Session = Depends(get_db)) -> CategorySchema:
    category_for_update = db.get(CategoryORM, category_id)
    if category_for_update is not None:
        if payload.name is not None:
            category_for_update.name = payload.name
            db.commit()
            return category_orm_to_model(category_for_update)

@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, db: Session = Depends(get_db)):
    category_for_delete = db.get(CategoryORM, category_id)
    if category_for_delete is not None:
        db.delete(category_for_delete)
        db.commit()
