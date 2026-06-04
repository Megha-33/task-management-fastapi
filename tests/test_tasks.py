import pytest
from uuid import uuid4


# Test cases for task management endpoints (CRUD operations)
@pytest.mark.asyncio
async def test_create_task_success(
    client,
    auth_headers
):
    response = await client.post(
        "/api/v1/tasks",
        json={
            "title": "Learn FastAPI",
            "description": "Practice Project",
            "priority": "HIGH"
        },
        headers=auth_headers
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Learn FastAPI"
    assert data["priority"] == "HIGH"


@pytest.mark.asyncio
async def test_create_task_without_title(
    client,
    auth_headers
):
    response = await client.post(
        "/api/v1/tasks",
        json={
            "description": "Missing title"
        },
        headers=auth_headers
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_task_empty_title(
    client,
    auth_headers
):
    response = await client.post(
        "/api/v1/tasks",
        json={
            "title": ""
        },
        headers=auth_headers
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_task_without_token(
    client
):
    response = await client.post(
        "/api/v1/tasks",
        json={
            "title": "Unauthorized Task"
        }
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_tasks_success(
    client,
    auth_headers
):
    response = await client.get(
        "/api/v1/tasks",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "page" in data
    assert "size" in data
    assert isinstance(data["items"], list)
    
    
@pytest.mark.asyncio
async def test_get_task_by_id(
    client,
    auth_headers
):
    create_response = await client.post(
        "/api/v1/tasks",
        json={
            "title": "Task One"
        },
        headers=auth_headers
    )

    task_id = create_response.json()["id"]

    response = await client.get(
        f"/api/v1/tasks/{task_id}",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id


@pytest.mark.asyncio
async def test_get_task_not_found(
    client,
    auth_headers
):
    fake_id = str(uuid4())

    response = await client.get(
        f"/api/v1/tasks/{fake_id}",
        headers=auth_headers
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_task_success(
    client,
    auth_headers
):
    create_response = await client.post(
        "/api/v1/tasks",
        json={
            "title": "Old Title"
        },
        headers=auth_headers
    )

    task_id = create_response.json()["id"]

    response = await client.put(
        f"/api/v1/tasks/{task_id}",
        json={
            "title": "New Title"
        },
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "New Title"


@pytest.mark.asyncio
async def test_partial_update_task(
    client,
    auth_headers
):
    create_response = await client.post(
        "/api/v1/tasks",
        json={
            "title": "Task",
            "status": "TODO"
        },
        headers=auth_headers
    )

    task_id = create_response.json()["id"]

    response = await client.put(
        f"/api/v1/tasks/{task_id}",
        json={
            "status": "COMPLETED"
        },
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "COMPLETED"


@pytest.mark.asyncio
async def test_update_task_not_found(
    client,
    auth_headers
):
    fake_id = str(uuid4())

    response = await client.put(
        f"/api/v1/tasks/{fake_id}",
        json={
            "title": "Updated"
        },
        headers=auth_headers
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_task_success(
    client,
    auth_headers
):
    create_response = await client.post(
        "/api/v1/tasks",
        json={
            "title": "Delete Me"
        },
        headers=auth_headers
    )

    task_id = create_response.json()["id"]

    response = await client.delete(
        f"/api/v1/tasks/{task_id}",
        headers=auth_headers
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_deleted_task_not_accessible(
    client,
    auth_headers
):
    create_response = await client.post(
        "/api/v1/tasks",
        json={
            "title": "Delete Task"
        },
        headers=auth_headers
    )

    task_id = create_response.json()["id"]

    await client.delete(
        f"/api/v1/tasks/{task_id}",
        headers=auth_headers
    )

    response = await client.get(
        f"/api/v1/tasks/{task_id}",
        headers=auth_headers
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_invalid_uuid(
    client,
    auth_headers
):
    response = await client.get(
        "/api/v1/tasks/invalid-id",
        headers=auth_headers
    )

    assert response.status_code == 422