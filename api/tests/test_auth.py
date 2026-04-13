import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def test_login_success(client: AsyncClient):
    """Korisnik se uspješno prijavljuje — 200."""
    resp = await client.post(
        "/auth/login",
        data={"username": "maki@gmail.com", "password": "password123"},
    )
    assert resp.status_code == 200
    assert "access_token" in resp.json()

async def test_get_me(client: AsyncClient, auth_header):
    """Dohvat vlastitih podataka s tokenom — 200."""
    headers = await auth_header(client, "maki@gmail.com", "password123")
    resp = await client.get("/auth/me", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["email"] == "maki@gmail.com"