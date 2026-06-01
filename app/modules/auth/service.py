from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.user import User
from app.modules.auth.schema import UserRegisterSchema
from app.core.security import hash_password


class AuthService:

    @staticmethod
    async def register_user(
        user_data: UserRegisterSchema,
        db: AsyncSession
    ) -> User:

        # Check existing email
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

        # Create new user
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