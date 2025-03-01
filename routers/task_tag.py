from fastapi import APIRouter, Depends, Path, Query
import crud
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session

router = APIRouter(prefix="/task-tags", tags=["Association Table"])


@router.post("/{task_id}/{tag_id}")
async def add_task_tag(
    task_id: int, tag_id: int, session: AsyncSession = Depends(get_session)
):
    return await crud.add_task_tag_crud(task_id=task_id, tag_id=tag_id, session=session)


@router.get("/task/{task_id}")
async def get_tags_for_task(task_id: int, session: AsyncSession = Depends(get_session)):
    return await crud.get_list_tags_for_task_crud(task_id=task_id, session=session)


@router.get("/tag/{tag_id}")
async def get_tasks_for_tag(tag_id: int, session: AsyncSession = Depends(get_session)):
    return await crud.get_list_task_for_tag_crud(tag_id=tag_id, session=session)
