from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from api import api_router
from cache.redis import redis_client
from database import db


@asynccontextmanager
async def lifespan(_: FastAPI):
    FastAPICache.init(backend=RedisBackend(redis_client), prefix="fastapi-cache")
    await db.create_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
