from fastapi import FastAPI
import uvicorn
import models
from models.base import Base
from contextlib import asynccontextmanager
from database import engine
from routers.user import router as user_router


# функция для работы с БД
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
