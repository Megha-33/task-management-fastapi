from pydantic import BaseModel

from app.modules.tasks.schema import (
    TaskResponseSchema
)


class PaginatedTaskResponse(BaseModel):
    items: list[TaskResponseSchema]
    total: int
    page: int
    size: int
    pages: int