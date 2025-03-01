from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import CreateUser, UpdateUserFull, UpdateUserPartial
from fastapi import HTTPException
from models.user import UserOrm
from models.task import TaskOrm
from sqlalchemy import select
from sqlalchemy.orm import selectinload


async def create_user_crud(user: CreateUser, session: AsyncSession):
    new_user = UserOrm(**user.model_dump())
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def user_presence_crud(user_id: int, session: AsyncSession):
    user = await session.get(UserOrm, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


async def get_user_by_id_crud(user_id: int, session: AsyncSession):
    user = await user_presence_crud(user_id, session)
    stmt = (
        select(UserOrm)
        .where(UserOrm.id == user_id)
        .options(selectinload(UserOrm.tasks).selectinload(TaskOrm.tags))
    )
    result = await session.execute(stmt)
    user_with_tasks = result.scalars().first()
    return user_with_tasks


async def get_list_users_crud(session: AsyncSession, start: int, stop: int):
    stmt = (
        select(UserOrm)
        .options(selectinload(UserOrm.tasks).selectinload(TaskOrm.tags))
        .offset(start)
        .limit(stop - start)
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def update_user_partial_crud(
    user: UpdateUserPartial, user_id: int, session: AsyncSession
):
    user_in = await user_presence_crud(user_id, session)
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(user_in, key, value)
    await session.commit()
    await session.refresh(user_in)
    return user_in


async def update_user_full_crud(
    user: UpdateUserFull, user_id: int, session: AsyncSession
):
    user_in = await user_presence_crud(user_id, session)
    for key, value in user.model_dump().items():
        setattr(user_in, key, value)
    await session.commit()
    await session.refresh(user_in)
    return user_in


async def delete_user_crud(user_id: int, session: AsyncSession):
    user = await user_presence_crud(user_id, session)
    await session.delete(user)
    await session.commit()
    return {"message": "Пользователь удален"}
