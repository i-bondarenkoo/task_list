from fastapi import APIRouter, HTTPException
from schemas.tag import CreateTag, UpdatePartialTag
from sqlalchemy.ext.asyncio import AsyncSession
from models.tag import TagOrm
from sqlalchemy import select
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/tags", tags=["Tags"])


async def create_tag_crud(tag: CreateTag, session: AsyncSession):
    new_tag = TagOrm(**tag.model_dump())
    session.add(new_tag)
    await session.commit()
    await session.refresh(new_tag)
    return new_tag


async def check_tag_crud(tag_id: int, session: AsyncSession):
    tag = await session.get(TagOrm, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Тег не найден")
    return tag


async def get_tag_by_id_crud(tag_id: int, session: AsyncSession):
    tag_in = await check_tag_crud(tag_id, session)
    stmt = select(TagOrm).where(TagOrm.id == tag_id).options(selectinload(TagOrm.tasks))
    result = await session.execute(stmt)
    tag_with_task = result.scalars().first()
    return tag_with_task


async def get_tag_pagination_crud(session: AsyncSession, start: int = 0, stop: int = 3):
    if start >= stop:
        raise HTTPException(status_code=400, detail="Неверные значения пагинации")
    stmt = (
        select(TagOrm)
        .options(selectinload(TagOrm.tasks))
        .offset(start)
        .limit(stop - start)
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def update_partial_tag_crud(
    tag: UpdatePartialTag, tag_id: int, session: AsyncSession
):
    tag_in = await check_tag_crud(tag_id, session)
    for key, value in tag.model_dump(exclude_unset=True).items():
        setattr(tag_in, key, value)
    await session.commit()
    await session.refresh(tag_in)
    return tag_in


async def delete_tag_crud(tag_id: int, session: AsyncSession):
    tag = await check_tag_crud(tag_id, session)
    await session.delete(tag)
    await session.commit()
    return {"message": "Тег удален"}
