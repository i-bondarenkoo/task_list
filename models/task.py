from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from sqlalchemy import ForeignKey
from models.associations import task_tag_table
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.tag import TagOrm
    from models.user import UserOrm


class TaskOrm(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(100))
    # ondelete="CASCADE"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped["UserOrm"] = relationship("UserOrm", back_populates="tasks")

    tags: Mapped[list["TagOrm"]] = relationship(
        "TagOrm", secondary=task_tag_table, back_populates="tasks"
    )

    def __repr__(self) -> str:
        return f"TaskOrm(id={self.id!r}, title={self.title!r}, description={self.description!r})"
