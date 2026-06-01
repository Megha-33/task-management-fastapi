from fastapi import (
    APIRouter,
    Depends
)

from app.models.user import (
    User,
    UserRole
)

from app.core.dependencies import (
    require_roles
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.modules.admin.schema import (
    AdminUserResponseSchema
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/dashboard")
async def admin_dashboard(
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    )
):

    return {
        "message": "Welcome Admin",
        "user": current_user.email
    }
    
@router.get(
    "/users",
    response_model=list[
        AdminUserResponseSchema
    ]
)
async def get_all_users(
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(User)
    )

    return result.scalars().all()