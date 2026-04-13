from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])


def get_repo(db: AsyncSession = Depends(get_db)) -> TaskRepository:
    return TaskRepository(db)


@router.get("/", response_model=list[TaskResponse])
async def list_tasks(
    skip: int = 0,
    limit: int = 100,
    repo: TaskRepository = Depends(get_repo),
):
    """Получить список всех задач."""
    return await repo.get_all(skip=skip, limit=limit)


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    data: TaskCreate,
    repo: TaskRepository = Depends(get_repo),
):
    """Создать новую задачу."""
    return await repo.create(data)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    repo: TaskRepository = Depends(get_repo),
):
    """Получить задачу по ID."""
    task = await repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    data: TaskUpdate,
    repo: TaskRepository = Depends(get_repo),
):
    """Обновить задачу (частично)."""
    task = await repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return await repo.update(task, data)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    repo: TaskRepository = Depends(get_repo),
):
    """Удалить задачу."""
    task = await repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    await repo.delete(task)