import pytest
from uuid import uuid4


# Test cases for authentication endpoints(registration and login)
@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "name": "John",
            "email": f"{uuid4()}@test.com",    # unique every run
            "password": "Password123"
        }
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_login(client):
    email = f"{uuid4()}@test.com"
    password = "Password123"

    await client.post(
        "/api/v1/auth/register",
        json={"name": "John", "email": email, "password": password}
    )

    response = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password}
    )

    assert response.status_code == 200
    assert "access_token" in response.json()