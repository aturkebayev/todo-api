from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import task


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="Todo API",
    version="1.0.0",
    description="Учебный REST API на FastAPI + PostgreSQL",
    lifespan=lifespan,
)

# CORS — разрешаем запросы из браузера (Swagger UI, фронтенд)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # В проде заменить на конкретный домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task.router)


@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok"}