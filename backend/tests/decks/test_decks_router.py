import pytest
import pytest_asyncio
from fastapi import status
from httpx import AsyncClient

from src.decks.schemas import DecksFilter, DeckView


@pytest_asyncio.fixture
async def deck(async_client: AsyncClient, random_deck_name: str):
    data = {"name": random_deck_name}
    response = await async_client.post("/api/decks", json=data)
    return response.json()


@pytest_asyncio.fixture
async def decks(async_client: AsyncClient):
    response = await async_client.get(url="/api/decks")
    return response.json()


@pytest.mark.asyncio
async def test_create_deck(async_client: AsyncClient, random_deck_name: str):
    data = {
        "name": random_deck_name,
    }
    response = await async_client.post(url="/api/decks", json=data)
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    DeckView.model_validate(obj=data)


@pytest.mark.asyncio
async def test_create_deck_with_same_name(async_client: AsyncClient, deck: dict):
    data = {
        "name": deck["name"],
    }
    second_response = await async_client.post(url="/api/decks", json=data)
    assert second_response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_get_deck(async_client: AsyncClient, deck: dict):
    deck_id = deck["id"]

    response = await async_client.get(f"/api/decks/{deck_id}")
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    DeckView.model_validate(obj=response_data)


@pytest.mark.asyncio
async def test_get_deck_non_existing(async_client: AsyncClient, generated_deck_id):
    response = await async_client.get(url=f"/api/decks/{generated_deck_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_decks(async_client: AsyncClient):
    response = await async_client.get(url="/api/decks")
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert isinstance(response_data, list)

    for item in response_data:
        DeckView.model_validate(obj=item)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["filter"],
    [
        (DecksFilter(offset=0, limit=10),),
        (DecksFilter(offset=0, limit=10),),
    ],
)
async def test_get_decks_with_filter(
    filter: DecksFilter, async_client: AsyncClient, decks
):
    params = filter.model_dump(exclude_none=True)
    response = await async_client.get(url="/api/decks", params=params)

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert isinstance(response_data, list)

    for item in response_data:
        DeckView.model_validate(obj=item)

    assert decks[filter.offset : filter.limit] == response_data
