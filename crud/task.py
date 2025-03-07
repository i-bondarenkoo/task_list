from sqlalchemy.ext.asyncio import AsyncSession
from models.task import TaskOrm
from sqlalchemy import select
from schemas.task import CreateTask, UpdatePartialTask
from crud.user import user_presence_crud
from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from models.tag import TagOrm


async def create_task_user(task: CreateTask, session: AsyncSession):
    await user_presence_crud(task.user_id, session)
    new_task = TaskOrm(**task.model_dump())
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)
    return new_task


async def task_presence_crud(task_id: int, session: AsyncSession):
    task = await session.get(TaskOrm, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task


async def get_task_by_id_crud(task_id: int, session: AsyncSession):
    task = await task_presence_crud(task_id, session)
    stmt = (
        select(TaskOrm)
        .where(TaskOrm.id == task_id)
        .options(
            # selectinload(TaskOrm.user),  # Загружаем данные о пользователе
            selectinload(TaskOrm.tags),
        )
    )
    result = await session.execute(stmt)
    task_with_tag = result.scalars().first()
    return task_with_tag


async def get_list_pagination_task_crud(
    session: AsyncSession, start: int = 0, stop: int = 3
):
    if start >= stop:
        raise HTTPException(status_code=400, detail="Неверные значения пагинации")
    stmt = (
        select(TaskOrm)
        .options(
            # selectinload(TaskOrm.user),
            selectinload(TaskOrm.tags),
        )
        .order_by(TaskOrm.id)
        .offset(start)
        .limit(stop - start)
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def partial_update_task_crud(
    task: UpdatePartialTask, task_id: int, session: AsyncSession
):
    # Проверяем существование задачи
    task_in = await task_presence_crud(task_id=task_id, session=session)

    # Проверяем, передан ли user_id в обновляемых данных
    update_data = task.model_dump(exclude_unset=True)
    # Здесь мы проверяем, передан ли новый user_id в запросе.
    #  Если передан, то проверяем, существует ли пользователь с таким ID.
    # Если его нет — выбрасывается HTTPException(404, "Пользователь не найден")
    if "user_id" in update_data:
        user_in = await user_presence_crud(
            user_id=update_data["user_id"], session=session
        )

    for key, value in update_data.items():
        setattr(task_in, key, value)

    await session.commit()
    await session.refresh(task_in)
    return task_in


async def delete_task_crud(task_id: int, session: AsyncSession):
    task_in = await task_presence_crud(task_id, session)
    await session.delete(task_in)
    await session.commit()
    return {"message": "Задача удалена"}
