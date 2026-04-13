from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings


# Движок — это соединение с БД. echo=True выводит SQL в консоль (удобно при разработке)
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Фабрика сессий — через неё выполняются все запросы к БД
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Базовый класс для всех моделей
class Base(DeclarativeBase):
    pass


# Dependency — FastAPI вызывает эту функцию для каждого запроса
async def get_db() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        yield session