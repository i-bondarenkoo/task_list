__all__ = (
    "CreateTag",
    "ResponseTag",
    "UpdatePartialTag",
    "ResponseTagWithRelationship",
    "CreateTask",
    "ResponseTask",
    "UpdatePartialTask",
    "ResponseTaskWithRelationship",
    "CreateUser",
    "ResponseUser",
    "UpdateUserPartial",
    "UpdateUserFull",
    "ResponseUserWithRelationship",
    "UserSchema",
)
from schemas.tag import (
    CreateTag,
    ResponseTag,
    UpdatePartialTag,
    ResponseTagWithRelationship,
)
from schemas.task import (
    CreateTask,
    ResponseTask,
    UpdatePartialTask,
    ResponseTaskWithRelationship,
)
from schemas.user import (
    CreateUser,
    ResponseUser,
    UpdateUserPartial,
    UpdateUserFull,
    ResponseUserWithRelationship,
    UserSchema,
)

ResponseUserWithRelationship.model_rebuild()
ResponseTaskWithRelationship.model_rebuild()
ResponseTagWithRelationship.model_rebuild()
