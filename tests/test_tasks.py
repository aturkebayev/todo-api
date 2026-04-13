import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_create_task(client: AsyncClient):
    payload = {"title": "Купить молоко", "description": "2 литра"}
    response = await client.post("/tasks/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Купить молоко"
    assert data["is_completed"] is False
    assert "id" in data


@pytest.mark.asyncio
async def test_list_tasks(client: AsyncClient):
    await client.post("/tasks/", json={"title": "Задача 1"})
    await client.post("/tasks/", json={"title": "Задача 2"})

    response = await client.get("/tasks/")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_get_task_by_id(client: AsyncClient):
    create_response = await client.post("/tasks/", json={"title": "Тест"})
    task_id = create_response.json()["id"]

    response = await client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id


@pytest.mark.asyncio
async def test_get_task_not_found(client: AsyncClient):
    response = await client.get("/tasks/9999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_task(client: AsyncClient):
    create_response = await client.post("/tasks/", json={"title": "Старый заголовок"})
    task_id = create_response.json()["id"]

    response = await client.patch(
        f"/tasks/{task_id}",
        json={"title": "Новый заголовок", "is_completed": True},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Новый заголовок"
    assert response.json()["is_completed"] is True


@pytest.mark.asyncio
async def test_delete_task(client: AsyncClient):
    create_response = await client.post("/tasks/", json={"title": "Удалить меня"})
    task_id = create_response.json()["id"]

    delete_response = await client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204

    get_response = await client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404