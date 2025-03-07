from fastapi import FastAPI
import uvicorn
import models
from models.base import Base
from contextlib import asynccontextmanager
from database import engine
from routers.user import router as user_router
from routers.task import router as task_router
from routers.tag import router as tag_router
from routers.task_tag import router as task_tag_router


# функция для работы с БД
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     await engine.dispose()


# app = FastAPI(lifespan=lifespan)
app = FastAPI()
app.include_router(user_router)
app.include_router(task_router)
app.include_router(tag_router)
app.include_router(task_tag_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
