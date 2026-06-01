from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserRegisterSchema(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=100
    )

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=100
    )


class UserResponseSchema(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    is_active: bool
    is_verified: bool
    model_config = {
        "from_attributes": True
    }
    
    
class LoginSchema(BaseModel):
    email: EmailStr
    password: str
    
class TokenSchema(BaseModel):
    access_token: str
    token_type: str