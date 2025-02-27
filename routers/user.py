from fastapi import APIRouter, Depends, Path, Query, HTTPException
import crud
from database import get_session
from schemas.user import CreateUser, ResponseUser, UpdateUserFull, UpdateUserPartial
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=ResponseUser)
async def create_user(user: CreateUser, session: AsyncSession = Depends(get_session)):
    return await crud.create_user_crud(user=user, session=session)


@router.get("/{user_id}", response_model=ResponseUser)
async def get_user_by_id(
    user_id: int = Path(..., description="ID Пользователя"),
    session: AsyncSession = Depends(get_session),
):
    return await crud.get_user_by_id_crud(user_id=user_id, session=session)


@router.get("/", response_model=list[ResponseUser])
async def get_all_users_pagination(
    start: int = Query(description="Начальный индекс"),
    stop: int = Query(description="Конечный индекс"),
    session: AsyncSession = Depends(get_session),
):
    if start >= stop:
        raise HTTPException(status_code=400, detail="Неверные значения пагинации")

    return await crud.get_list_users_crud(session=session, start=start, stop=stop)


@router.patch("/{user_id}", response_model=ResponseUser)
async def update_user_partial(
    user: UpdateUserPartial, user_id: int, session: AsyncSession = Depends(get_session)
):
    return await crud.update_user_partial_crud(
        user=user, user_id=user_id, session=session
    )


@router.put("/{user_id}", response_model=ResponseUser)
async def update_user(
    user: UpdateUserFull, user_id: int, session: AsyncSession = Depends(get_session)
):
    return await crud.update_user_full_crud(user=user, user_id=user_id, session=session)


@router.delete("/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    return await crud.delete_user_crud(user_id=user_id, session=session)
