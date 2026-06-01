from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.user import User
from app.modules.auth.schema import UserRegisterSchema
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


class AuthService:

    @staticmethod
    async def register_user(
        user_data: UserRegisterSchema,
        db: AsyncSession
    ) -> User:

        result = await db.execute(
            select(User).where(
                User.email == user_data.email
            )
        )

        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password=hash_password(
                user_data.password
            )
        )

        db.add(new_user)

        await db.commit()

        await db.refresh(new_user)

        return new_user

    @staticmethod
    async def login_user(
        email: str,
        password: str,
        db: AsyncSession
    ):

        result = await db.execute(
            select(User).where(
                User.email == email
            )
        )

        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        if not verify_password(
            password,
            user.password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }