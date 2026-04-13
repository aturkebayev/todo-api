from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import task


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Выполняется при старте: создаём таблицы если их нет
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Выполняется при остановке: закрываем соединения
    await engine.dispose()


app = FastAPI(
    title="Todo API",
    version="1.0.0",
    description="Учебный REST API на FastAPI + PostgreSQL",
    lifespan=lifespan,
)

app.include_router(task.router)


@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok"}