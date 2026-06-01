from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User

from enum import Enum
from datetime import datetime

from sqlalchemy import (
    UUID,
    String,
    Text,
    DateTime,
    ForeignKey,
    Enum as SqlEnum
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.models.base import BaseModel


class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class TaskPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Task(BaseModel):
    __tablename__ = "tasks"

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    status: Mapped[TaskStatus] = mapped_column(
        SqlEnum(TaskStatus),
        default=TaskStatus.TODO
    )

    priority: Mapped[TaskPriority] = mapped_column(
        SqlEnum(TaskPriority),
        default=TaskPriority.MEDIUM
    )

    due_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    user_id: Mapped[UUID] = mapped_column(
    UUID(as_uuid=True),
    ForeignKey("users.id"),
    nullable=False
    )
    
    user: Mapped["User"] = relationship(
    back_populates="tasks"
    )
