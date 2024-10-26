from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api import routers as api_routers
from database import on_startup, db_helper


def create_app() -> FastAPI:

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # startup
        await on_startup()

        yield
        # shutdown
        await db_helper.dispose()

    app = FastAPI(
        title="Books_base API",
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
        description="Books_base API is an interface for managing the functionality of the Telegram bot, providing access to the electronic book library. The API enables integration and automation of interactions with the store, offering features for fast search, order processing, purchase management, and tracking user status.",
        version="1.0.0",
    )

    app.include_router(api_routers)

    return app
