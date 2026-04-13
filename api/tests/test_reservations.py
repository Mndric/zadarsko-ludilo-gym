import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def test_create_reservation(client: AsyncClient, user_and_membership, auth_header):
    """Korisnik kreira rezervaciju — 201."""
    user, _ = user_and_membership
    headers = await auth_header(client, user.email, "password123")
    resp = await client.post(
        "/gym/reserve",
        json={"equipment_id": 1, "reservation_date": "2026-05-01T10:00:00"},
        headers=headers,
    )
    assert resp.status_code == 201

async def test_list_my_reservations(client: AsyncClient, user_and_membership, reservation, auth_header):
    user, _ = user_and_membership
    headers = await auth_header(client, user.email, "password123")
    resp = await client.get("/gym/my-reservations", headers=headers)
    assert resp.status_code == 200

async def test_update_reservation(client: AsyncClient, user_and_membership, reservation, auth_header):
    user, _ = user_and_membership
    headers = await auth_header(client, user.email, "password123")
    resp = await client.put(
        f"/gym/reservations/{reservation.id}?new_date=2026-06-01T10:00:00",
        headers=headers,
    )
    assert resp.status_code == 200

async def test_forbidden_access_other_reservation(client: AsyncClient, user_b_and_membership, reservation, auth_header):
    user_b, _ = user_b_and_membership
    headers = await auth_header(client, user_b.email, "password123")
    resp = await client.get(f"/gym/reservations/{reservation.id}", headers=headers)
    assert resp.status_code == 403

async def test_create_reservation_past_date(client: AsyncClient, user_and_membership, auth_header):
    user, _ = user_and_membership
    headers = await auth_header(client, user.email, "password123")
    resp = await client.post(
        "/gym/reserve",
        json={"equipment_id": 1, "reservation_date": "2020-01-01T10:00:00"},
        headers=headers,
    )
    assert resp.status_code in [400, 422]