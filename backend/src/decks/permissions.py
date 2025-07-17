from fastapi import Request

from auth.permissions import BasePermission

from decks.service import decks_service


class DeckOwnerPermission(BasePermission):
    async def has_required_permissions(self, request: Request) -> bool:
        """Check if a user is the owner of a deck"""
        deck_id = request.path_params["deck_id"]
        deck = await decks_service.get(deck_id=deck_id, uow=request.state.uow)

        return deck.user_id == request.user.id
