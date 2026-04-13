from datetime import datetime

from pydantic import BaseModel, Field


# Базовые поля, общие для создания и обновления
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Название задачи")
    description: str | None = Field(None, max_length=1000, description="Описание задачи")


# Схема для создания задачи (POST /tasks)
class TaskCreate(TaskBase):
    pass


# Схема для обновления задачи (PATCH /tasks/{id})
class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = Field(None, max_length=1000)
    is_completed: bool | None = None


# Схема для ответа клиенту (что возвращаем из API)
class TaskResponse(TaskBase):
    id: int
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}  # Позволяет создавать схему из ORM-объекта