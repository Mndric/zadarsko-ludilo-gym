import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from main import app
import asyncio

@pytest.fixture(scope="session")
def event_loop():
    """Kreira instancu event loopa za cijelu testnu sesiju."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def auth_header():
    async def _header(client: AsyncClient, email: str, password: str):
        login_data = {"username": email, "password": password}
        # Dodajemo mali osigurač da sačekamo klijenta
        resp = await client.post("/auth/login", data=login_data)
        if resp.status_code != 200:
            raise Exception(f"Login failed for test: {resp.text}")
        token = resp.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    return _header

@pytest.fixture
def user_and_membership():
    class MockUser:
        email = "maki@gmail.com"
        id = 1
    return MockUser(), None

@pytest.fixture
def user_b_and_membership():
    class MockUserB:
        email = "drugi@gmail.com"
        id = 2
    return MockUserB(), None

@pytest.fixture
def reservation():
    class MockRes:
        id = 1
    return MockRes()

@pytest.fixture
def admin_user():
    return {"email": "admin@gym.com", "id": 99}