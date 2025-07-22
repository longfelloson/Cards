from fastapi import Request

from auth.permissions import BasePermission, OwnerPermission, UserMatchPermission, VisibilityPermission, any_permission

from decks.service import decks_service


class DeckOwnerPermission(BasePermission):
    async def has_required_permissions(self, request: Request) -> bool:
        """Check if a user is the owner of a deck"""
        deck_id = request.path_params["deck_id"]
        deck = await decks_service.get(deck_id=deck_id, uow=request.state.uow)

        return deck.user_id == request.user.id


class DeckViewPermission(BasePermission):
    async def has_required_permissions(self, request: Request):
        """
        Check if user is an admin or owns the deck
        """
        deck_id = request.path_params["deck_id"]
        card = await decks_service.get(deck_id=deck_id, uow=request.state.uow)

        has_permission = await any_permission(
            permissions=[
                OwnerPermission(instance=card),
                VisibilityPermission(instance=card)
            ],
            request=request,
        )
        return has_permission


class DecksViewPermission(BasePermission):
    async def has_required_permissions(self, request: Request) -> bool:
        """
        Check if user requires its own decks or not hidden decks
        """
        has_permission = await any_permission(
            permissions=[
                UserMatchPermission(),
                VisibilityPermission(),
            ],
            request=request,
        )
        return has_permission
    