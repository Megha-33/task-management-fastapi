from datetime import datetime
from uuid import UUID

from pydantic import (
    BaseModel,
    Field,
    ConfigDict
)

from app.models.task import (
    TaskStatus,
    TaskPriority
)


class TaskCreateSchema(BaseModel):

    title: str = Field(
        min_length=3,
        max_length=255
    )

    description: str | None = None

    priority: TaskPriority = (
        TaskPriority.MEDIUM
    )

    due_date: datetime | None = None
    
class TaskUpdateSchema(BaseModel):

    title: str | None = Field(
        default=None,
        min_length=3,
        max_length=255
    )

    description: str | None = None

    status: TaskStatus | None = None

    priority: TaskPriority | None = None

    due_date: datetime | None = None
    
    
class TaskResponseSchema(BaseModel):

    id: UUID

    title: str

    description: str | None

    status: TaskStatus

    priority: TaskPriority

    due_date: datetime | None

    user_id: UUID

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )