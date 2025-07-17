from fastapi import APIRouter, Depends
from auth.router import router as auth_router
from auth.rbac.dependencies import RoleAccessDependency
from cards.router import v1_router as v1_cards_router
from deck_collections.router import v1_router as v1_collections_router
from decks.router import v1_router as v1_decks_router
from users.router import v1_router as v1_users_router

api_v1_router = APIRouter()

api_v1_router.include_router(auth_router, prefix="/auth", tags=["Auth"])

api_v1_router.include_router(
    v1_cards_router,
    prefix="/cards",
    tags=["Cards"],
    dependencies=[Depends(RoleAccessDependency())],
)

api_v1_router.include_router(
    v1_decks_router,
    prefix="/decks",
    tags=["Decks"],
    dependencies=[Depends(RoleAccessDependency())],
)

api_v1_router.include_router(
    v1_users_router,
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(RoleAccessDependency())],
)

api_v1_router.include_router(
    v1_collections_router,
    prefix="/collections",
    tags=["Collections"],
    dependencies=[Depends(RoleAccessDependency())],
)
