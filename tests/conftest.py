import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from database.db_helper import db_helper
from database.models._base import Base
from api.main import app

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./tests/test.db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)

TestingSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


@pytest.fixture(scope="function", autouse=True)
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def db_session():
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession):
    app.dependency_overrides[db_helper.session_getter] = lambda: db_session
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client
