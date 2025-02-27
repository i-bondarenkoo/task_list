import crud
from fastapi import Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from fastapi import APIRouter
from schemas.tag import CreateTag, ResponseTag, UpdatePartialTag

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.post("/", response_model=ResponseTag)
async def create_tag(tag: CreateTag, session: AsyncSession = Depends(get_session)):
    return await crud.create_tag_crud(tag=tag, session=session)


@router.get("/{tag_id}", response_model=ResponseTag)
async def get_tag_by_id(
    tag_id: int = Path(..., description="ID Тега"),
    session: AsyncSession = Depends(get_session),
):
    return await crud.get_tag_by_id_crud(tag_id=tag_id, session=session)


@router.get("/", response_model=list[ResponseTag])
async def get_list_tags(
    session: AsyncSession = Depends(get_session),
    start: int = Query(0, description="Начальная позиция"),
    stop: int = Query(3, description="Конечная позиция"),
):
    return await crud.get_tag_pagination_crud(session=session, start=start, stop=stop)


@router.patch("/{tag_id}")
async def update_tag(
    tag: UpdatePartialTag,
    tag_id: int = Path(..., description="ID Тега"),
    session: AsyncSession = Depends(get_session),
):
    return await crud.update_partial_tag_crud(tag_id=tag_id, tag=tag, session=session)


@router.delete("/{tag_id}")
async def delete_tag(
    tag_id: int = Path(..., description="ID Тега"),
    session: AsyncSession = Depends(get_session),
):
    return await crud.delete_tag_crud(tag_id=tag_id, session=session)
