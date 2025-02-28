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
