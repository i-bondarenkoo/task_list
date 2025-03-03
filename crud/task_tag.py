from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete
from models.associations import task_tag_table
from crud.task import task_presence_crud
from crud.tag import get_tag_by_id_crud
from models.tag import TagOrm
from models.task import TaskOrm
from fastapi import HTTPException


async def add_task_tag_crud(task_id: int, tag_id: int, session: AsyncSession):
    """Добавляет связь между задачей и тегом"""
    # Проверка что тэг и задача существуют
    task = await task_presence_crud(task_id, session)
    tag = await get_tag_by_id_crud(tag_id, session)
    # Проверка на дублирующиеся записи
    double_record = select(task_tag_table).where(
        task_tag_table.c.task_id == task_id, task_tag_table.c.tag_id == tag_id
    )
    result = await session.execute(double_record)
    if result.scalar() is not None:
        raise HTTPException(status_code=400, detail="Такая запись уже существует")
    stmt = insert(task_tag_table).values(task_id=task_id, tag_id=tag_id)
    await session.execute(stmt)
    await session.commit()
    return {"message": "Данные успешно добавлены"}


async def get_list_tags_for_task_crud(task_id: int, session: AsyncSession):
    task = await task_presence_crud(task_id, session)
    stmt = (
        select(TagOrm)
        .join(task_tag_table, task_tag_table.c.tag_id == TagOrm.id)
        .where(task_tag_table.c.task_id == task_id)
    )
    result = await session.execute(stmt)
    list_tags = result.scalars().all()
    return list_tags


async def get_list_task_for_tag_crud(tag_id: int, session: AsyncSession):
    tag = await get_tag_by_id_crud(tag_id, session)
    stmt = (
        select(TaskOrm)
        .join(task_tag_table, task_tag_table.c.task_id == TaskOrm.id)
        .where(task_tag_table.c.tag_id == tag_id)
    )
    result = await session.execute(stmt)
    list_task = result.scalars().all()
    return list_task
