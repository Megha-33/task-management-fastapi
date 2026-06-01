from fastapi import APIRouter

from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.modules.admin.router import router as admin_router

# Main API router that includes all module routers
api_router = APIRouter()


api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(admin_router)