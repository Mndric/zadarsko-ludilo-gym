import pytest
from httpx import AsyncClient

async def test_list_equipment(client: AsyncClient):
    """Javni dohvat liste opreme — 200."""
    resp = await client.get("/gym/equipment")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

async def test_admin_create_equipment(client: AsyncClient, admin_user):
    """Samo admin može dodati opremu — 201."""
    from tests.conftest import auth_header
    headers = await auth_header(client, "admin@gym.com", "admin123")
    resp = await client.post(
        "/gym/equipment",
        json={"name": "Bučice", "quantity": 10},
        headers=headers,
    )
    assert resp.status_code == 201