from fastapi import APIRouter, Depends
from auth.rbac.dependencies import check_permissions
from auth.router import router as auth_router
from cards.router import v1_router as v1_cards_router
from deck_collections.router import v1_router as v1_collections_router
from decks.router import v1_router as v1_decks_router
from users.router import v1_router as v1_users_router

api_v1_router = APIRouter()

api_v1_router.include_router(auth_router, prefix="/auth", tags=["Auth"])

protected_routers = [
    {"router": v1_cards_router, "prefix": "/cards", "tags": ["Cards"]},
    {"router": v1_decks_router, "prefix": "/decks", "tags": ["Decks"]},
    {"router": v1_users_router, "prefix": "/users", "tags": ["Users"]},
    {
        "router": v1_collections_router,
        "prefix": "/collections",
        "tags": ["Collections"],
    },
]

for router in protected_routers:
    api_v1_router.include_router(**router, dependencies=[Depends(check_permissions)])
