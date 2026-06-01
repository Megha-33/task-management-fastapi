from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.models.user import UserRole


class CurrentUserResponseSchema(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    is_verified: bool

    model_config = {
        "from_attributes": True
    }