from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from cashews import cache
from starlette.middleware.authentication import AuthenticationMiddleware

from api import api_v1_router
from auth.middlewares import AuthMiddleware
from auth.permissions.exceptions import NotEnoughPermissionsException
from auth.rbac.exceptions import ResourceNotFound
from database import db
from config import settings
from logger import logger


cache.setup(settings.redis.url)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await db.create_tables()

    yield


app_config = {"title": "Cards"}
if settings.ENVIRONMENT != "local":
    app_config["openapi_url"] = None


app = FastAPI(lifespan=lifespan, **app_config)

versioned_routers = {"1": api_v1_router}
app.include_router(
    versioned_routers[str(settings.API_VERSION)], prefix=settings.api_prefix
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.all_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    AuthenticationMiddleware,
    backend=AuthMiddleware(),
)


@app.exception_handler(NotEnoughPermissionsException)
async def permission_exceptions_handler(
    request: Request, exception: NotEnoughPermissionsException
):
    logger.warning(f"User with id = {request.user.id} didn't have {exception.permission}")
    raise ResourceNotFound()
