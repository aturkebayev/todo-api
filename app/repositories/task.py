from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskRepository:
    """Весь код работы с БД сосредоточен здесь. Роутеры не знают про SQL."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Task]:
        result = await self.db.execute(select(Task).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def get_by_id(self, task_id: int) -> Task | None:
        result = await self.db.execute(select(Task).where(Task.id == task_id))
        return result.scalar_one_or_none()

    async def create(self, data: TaskCreate) -> Task:
        task = Task(**data.model_dump())
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)  # Обновляем объект из БД (получаем id, created_at)
        return task

    async def update(self, task: Task, data: TaskUpdate) -> Task:
        # exclude_unset=True — обновляем только те поля, которые пришли в запросе
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete(self, task: Task) -> None:
        await self.db.delete(task)
        await self.db.commit()