import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import TypedDict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import Redis

from wallstr.auth.api import router as auth_router
from wallstr.chat.api import router as chat_router
from wallstr.conf import settings
from wallstr.db import AsyncSessionMaker, create_async_engine, create_session_maker
from wallstr.documents.api import router as documents_router
from wallstr.logging import configure_logging
from wallstr.openapi import (
    configure_openapi,
    generate_unique_id_function,
)

configure_logging()
logger = logging.getLogger(__name__)


class AppState(TypedDict):
    redis: Redis
    session_maker: AsyncSessionMaker


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[AppState, None]:
    engine = create_async_engine(settings.DATABASE_URL, "wallstr")
    session_maker = create_session_maker(engine)

    redis = Redis.from_url(settings.REDIS_URL.get_secret_value())
    try:
        yield {
            "redis": redis,
            "session_maker": session_maker,
        }
    finally:
        try:
            await redis.aclose()
        except Exception as e:
            logger.exception(e)
        try:
            await engine.dispose()
        except Exception as e:
            logger.exception(e)


app = FastAPI(
    version=settings.VERSION,
    lifespan=lifespan,
    generate_unique_id_function=generate_unique_id_function(),
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "OPTIONS"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(documents_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": f"wallstr.chat v{settings.VERSION}"}


configure_openapi(app)
