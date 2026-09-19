from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema

from app.services.task import TaskNotFoundError, TaskService
from app.api.dependencies import get_task_service

task_router = APIRouter(prefix="/tasks", tags=["Tasks"])

@task_router.get("", status_code=status.HTTP_200_OK)
def read_tasks(service: TaskService = Depends(get_task_service)) -> list[TaskSchema]:
    return service.list_tasks()


@task_router.post("", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreateSchema, 
    service: TaskService = Depends(get_task_service),
) -> TaskSchema:
    return service.create_task(payload)


@task_router.patch("/{task_id}", status_code=status.HTTP_200_OK)
def update_task(
    task_id: str, 
    payload: TaskUpdateSchema, 
    service: TaskService = Depends(get_task_service),
) -> TaskSchema:
    try:
        return service.update_task(task_id, payload)
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена",
        )


@task_router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: str, 
    service: TaskService = Depends(get_task_service),
) -> None:
    try:
        service.delete_task(task_id=task_id)
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена",
        )
    