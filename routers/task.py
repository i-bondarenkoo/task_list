from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from schemas.task import CreateTask, ResponseTask, UpdatePartialTask
import crud


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.post("/", response_model=ResponseTask)
async def create_task(task: CreateTask, session: AsyncSession = Depends(get_session)):
    return await crud.create_task_user(task=task, session=session)


@router.get("/{task_id}", response_model=ResponseTask)
async def get_task_by_id(
    task_id: int = Path(..., description="ID Задачи"),
    session: AsyncSession = Depends(get_session),
):
    return await crud.get_task_by_id_crud(task_id=task_id, session=session)


@router.get("/", response_model=list[ResponseTask])
async def get_list_task(
    session: AsyncSession = Depends(get_session),  # Подключаем сессию через Depends
    start: int = Query(0, description="С какого ID начать список"),
    stop: int = Query(3, description="Каким ID закончить список"),
):
    return await crud.get_list_pagination_task_crud(
        session=session, start=start, stop=stop
    )


@router.patch("/{task_id}", response_model=ResponseTask)
async def update_task(
    task: UpdatePartialTask,
    task_id: int = Path(..., description="ID задачи для обновления"),
    session: AsyncSession = Depends(get_session),
):
    return await crud.partial_update_task_crud(
        task=task, task_id=task_id, session=session
    )


@router.delete("/{task_id}")
async def delete_task(
    task_id: int = Path(..., description="ID задачи для удаления"),
    session: AsyncSession = Depends(get_session),
):
    return await crud.delete_task_crud(task_id=task_id, session=session)
