from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.modules.auth.schema import (
    UserRegisterSchema,
    UserResponseSchema
)
from app.modules.auth.service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# User registration endpoint(similar to a controller)
@router.post(
    "/register",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED
)
async def register_user(
    user_data: UserRegisterSchema,
    db: AsyncSession = Depends(get_db)
):

    return await AuthService.register_user(
        user_data=user_data,
        db=db
    )