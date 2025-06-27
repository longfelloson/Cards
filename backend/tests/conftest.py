import uuid
from httpx import ASGITransport, AsyncClient
import pytest
import pytest_asyncio

from src.auth.token import create_access_token
from src.config import settings
from src.unit_of_work import UnitOfWork
from src.database import Base, engine
from src.main import app


USER_ID = "0f3a91c1-86f9-493c-8283-7057fdd63cf0"

# @pytest.fixture(scope="session", autouse=True)
# async def prepare_database():
#     assert settings.MODE == "TEST"

#     print("Before dropping")
#     async with engine.begin() as conn:
#         # This executes drop_all and create_all in a sync way inside an async connection
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#     print("After dropping")


@pytest.fixture
def uow():
    return UnitOfWork()


@pytest.fixture
def auth_headers():
    token = create_access_token(data={"sub": "kashirinivan@icloud.com"})
    return {"Authorization": f"Bearer {token.access_token}"}


@pytest_asyncio.fixture
async def async_client(auth_headers):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        headers=auth_headers,
    ) as client:
        yield client


@pytest.fixture
def generated_deck_id():
    return str(object=uuid.uuid4())
