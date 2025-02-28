from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete, update
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
    stmt = insert(task_tag_table).values(task_id=task_id, tag_id=tag_id)
    await session.execute(stmt)
    await session.commit()
    return {"message": "Данные успешно добавлены"}
