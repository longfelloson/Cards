from fastapi import APIRouter, Depends

from auth.router import router as auth_router
from auth.rbac.dependencies import check_permissions
from cards.router import router as cards_router
from deck_collections.router import router as collections_router
from decks.router import router as decks_router
from users.router import router as users_router


api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])

api_router.include_router(
    cards_router,
    prefix="/cards",
    tags=["Cards"],
    dependencies=[Depends(check_permissions)],
)

api_router.include_router(
    decks_router,
    prefix="/decks",
    tags=["Decks"],
    dependencies=[Depends(check_permissions)],
)

api_router.include_router(
    users_router,
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(check_permissions)],
)

api_router.include_router(
    collections_router,
    prefix="/collections",
    tags=["Collections"],
    dependencies=[Depends(check_permissions)],
)
