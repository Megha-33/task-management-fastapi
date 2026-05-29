from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.config import settings
from app.core.database import get_db

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)


@app.get("/")
async def root():
    return {
        "message": f"{settings.APP_NAME} is running"
    }


@app.get("/health/db")
async def db_health_check(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(text("SELECT 1"))

    return {
        "database": "connected",
        "result": result.scalar()
    }