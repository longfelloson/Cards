from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from api import api_v1_router
from cache.redis import redis_client
from database import db
from config import settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    FastAPICache.init(backend=RedisBackend(redis_client), prefix="fastapi-cache")
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
