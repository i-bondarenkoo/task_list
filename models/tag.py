from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base
from models.associations import task_tag_table

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.task import TaskOrm


class TagOrm(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    color: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    tasks: Mapped[list["TaskOrm"]] = relationship(
        "TaskOrm", secondary=task_tag_table, back_populates="tags"
    )

    def __repr__(self) -> str:
        return f"TagOrm(id={self.id!r}, name={self.name!r}, color={self.color!r})"
