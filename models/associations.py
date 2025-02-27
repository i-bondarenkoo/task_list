from sqlalchemy import Table, Column, Integer, ForeignKey
from models.base import Base

task_tag_table = Table(
    "task_tag",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)
