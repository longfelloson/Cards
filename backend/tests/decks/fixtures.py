from random import randint
import pytest

from decks.schemas import DecksFilter
from decks.service import DeckService


@pytest.fixture
def random_deck_name():
    base_name = "DECK NAME"
    random_number = randint(a=111111, b=999999)
    return f"{base_name} {random_number}"


@pytest.fixture
def deck_service():
    return DeckService()


@pytest.fixture
def decks_filter():
    return DecksFilter()
