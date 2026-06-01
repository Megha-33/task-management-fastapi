from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.task import Task

from enum import Enum
from sqlalchemy import String, Boolean, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"


class User(BaseModel):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    role: Mapped[UserRole] = mapped_column(
        SqlEnum(UserRole),
        default=UserRole.USER
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )
    
    tasks: Mapped[list["Task"]] = relationship(
    back_populates="user",
    cascade="all, delete-orphan"
    )