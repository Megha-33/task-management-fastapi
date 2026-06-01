from fastapi import (
    APIRouter,
    Depends
)

from app.models.user import User

from app.modules.users.schema import (
    CurrentUserResponseSchema
)

from app.core.dependencies import (
    get_current_user
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/me",
    response_model=CurrentUserResponseSchema
)
async def get_me(
    current_user: User = Depends(
        get_current_user
    )
):
    return current_user