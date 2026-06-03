from pydantic import BaseModel, Field

from app.models.task import (
    TaskStatus,
    TaskPriority
)


class TaskQueryParams(BaseModel):

    page: int = Field(
        default=1,
        ge=1
    )

    size: int = Field(
        default=10,
        ge=1,
        le=100
    )

    status: TaskStatus | None = None

    priority: TaskPriority | None = None

    search: str | None = None

    sort_by: str = "created_at"

    order: str = "desc"