from fastapi import Request

from auth.permissions import (
    BasePermission,
    OwnerPermission,
    UserMatchPermission,
    VisibilityPermission,
    any_permission,
)
from cards.service import cards_service


class CardOwnerPermission(BasePermission):
    async def has_required_permissions(self, request: Request) -> bool:
        card_id = request.path_params.get("card_id")
        card = await cards_service.get(card_id=card_id, uow=request.state.uow)

        return card.user_id == request.user.id


class CardViewPermission(BasePermission):
    async def has_required_permissions(self, request: Request):
        """
        Check if user is an admin or owns the card
        """
        card_id = request.path_params["card_id"]
        card = await cards_service.get(card_id=card_id, uow=request.state.uow)

        has_permission = await any_permission(
            permissions=[
                OwnerPermission(instance=card),
                VisibilityPermission(instance=card)
            ],
            request=request,
        )
        return has_permission


class CardsViewPermission(BasePermission):
    async def has_required_permissions(self, request: Request) -> bool:
        """
        Check if user requires its own cards or not hidden cards
        """
        has_permission = await any_permission(
            permissions=[
                UserMatchPermission(),
                VisibilityPermission(),
            ],
            request=request,
        )
        return has_permission
