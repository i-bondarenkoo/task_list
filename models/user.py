from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.task import TaskOrm


class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    tasks: Mapped[list["TaskOrm"]] = relationship(
        "TaskOrm", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"UserOrm(id={self.id!r}, first_name='{self.first_name!r}', last_name='{self.last_name!r}', email='{self.email!r}')"
