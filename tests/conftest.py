import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from uuid import uuid4

from app.main import app
from app.core.database import get_db
from app.core.config import settings

# NullPool = no connection reuse across tests
# Each request opens/closes its own connection — safe across event loops
test_engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    poolclass=NullPool,
    echo=False,
)

TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Overriding the get_db dependency to use the test database session
async def override_get_db():
    async with TestSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db


# Pytest fixtures for test client and authenticated headers
@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        yield client


@pytest.fixture
async def auth_headers(client):
    email = f"{uuid4()}@test.com"
    password = "Password123"

    await client.post(
        "/api/v1/auth/register",
        json={"name": "Test User", "email": email, "password": password}
    )

    login_response = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password}
    )

    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}