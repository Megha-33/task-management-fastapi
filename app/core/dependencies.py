
# The above code is an alternative implementation using OAuth2PasswordBearer.

# from fastapi.security import OAuth2PasswordBearer

# from jose import JWTError, jwt

# from fastapi import (
#     Depends,
#     HTTPException,
#     status
# )

# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.core.config import settings
# from app.core.database import get_db

# from app.models.user import User


# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl="/api/v1/auth/login"
# )

# async def get_current_user(
#     token: str = Depends(oauth2_scheme),
#     db: AsyncSession = Depends(get_db)
# ):

#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials"
#     )

#     try:

#         payload = jwt.decode(
#             token,
#             settings.JWT_SECRET_KEY,
#             algorithms=[settings.JWT_ALGORITHM]
#         )

#         user_id = payload.get("sub")

#         if user_id is None:
#             raise credentials_exception

#     except JWTError:
#         raise credentials_exception

#     result = await db.execute(
#         select(User).where(
#             User.id == user_id
#         )
#     )

#     user = result.scalar_one_or_none()

#     if not user:
#         raise credentials_exception

#     return user


#################################################################
# The current implementation uses HTTPBearer for simplicity.

from fastapi import (
    Depends,
    HTTPException,
    status
)

from fastapi.security import (
    HTTPBearer,
)

from jose import JWTError, jwt

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

from app.models.user import UserRole
security = HTTPBearer()

async def get_current_user(
    token: str = Depends(security),
    db: AsyncSession = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    
    try:
        

        payload = jwt.decode(
            token.credentials,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        user_id = payload.get("sub")

        if not user_id:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    result = await db.execute(
        select(User).where(
            User.id == user_id
        )
    )

    user = result.scalar_one_or_none()

    if not user:
        raise credentials_exception

    # NEW: Active user check
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    return user

def require_roles(*allowed_roles: UserRole):

    async def role_checker(
        current_user: User = Depends(
            get_current_user
        )
    ):

        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

        return current_user

    return role_checker