from pydantic import UUID4
import pytest
import random
import pytest_asyncio
from decks.exceptions import DeckNotFound
from decks.models import Deck
from decks.schemas import DeckCreate, DeckUpdate, DecksFilter
from decks.service import DeckService
from tests.conftest import USER_ID
from tests.decks.fixtures import random_deck_name, decks_filter, deck_service
from contextlib import nullcontext as does_not_raise


@pytest.fixture
def deck_create(random_deck_name):
    return DeckCreate(name=random_deck_name)


@pytest.fixture
def deck_update(random_deck_name):
    return DeckUpdate(name=random_deck_name)


@pytest_asyncio.fixture
async def random_deck_id(uow, decks_filter, deck_service: DeckService):
    decks = await deck_service.get_all(filter=decks_filter, user_id=USER_ID, uow=uow)

    random_deck: Deck = random.choice(decks)
    return random_deck.id


class TestDecksService:
    @pytest.mark.asyncio
    async def test_update(
        self, deck_update, random_deck_id, deck_service: DeckService, uow
    ):
        deck = await deck_service.get(deck_id=random_deck_id, uow=uow)
        assert deck is not None

        updated_deck = await deck_service.update(
            deck_id=deck.id, data=deck_update, uow=uow
        )
        assert updated_deck.name == deck_update.name

    @pytest.mark.asyncio
    async def test_create(self, deck_create, deck_service: DeckService, uow):
        deck = await deck_service.create(data=deck_create, user_id=USER_ID, uow=uow)
        assert isinstance(deck, Deck)

    @pytest.mark.asyncio
    async def test_get(self, random_deck_id, deck_service: DeckService, uow):
        deck = await deck_service.get(deck_id=random_deck_id, uow=uow)
        assert deck.id == random_deck_id

    @pytest.mark.asyncio
    async def test_get_no_existing(
        self, generated_deck_id, deck_service: DeckService, uow
    ):
        with pytest.raises(DeckNotFound):
            assert await deck_service.get(deck_id=generated_deck_id, uow=uow)
