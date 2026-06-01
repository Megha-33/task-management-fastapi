from fastapi import APIRouter

from app.modules.auth.router import router as auth_router

# Main API router that includes all module routers
api_router = APIRouter()


api_router.include_router(auth_router)