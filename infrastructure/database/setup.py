from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)

from tgbot.config import DbConfig, load_config


class DatabaseHelper:
    def __init__(self, db: DbConfig, echo: bool = False):
        self.engine = create_async_engine(
            url=db.construct_sqlalchemy_url(),
            # query_cache_size=1200,  # Устанавливает размер кэша запросов (2400)
            # pool_size=1000,  # Устанавливает максимальное количество соединений в пуле (150)
            # # max_overflow устанавливает максимальное количество соединений,
            # # которые могут быть созданы поверх установленного pool_size (500)
            # max_overflow=4000,
            # future=True,  # Включает использование объектов FutureResult для асинхронных запросов.
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,  # autoflush – подготовка к коммиту
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        await session.remove()


config = load_config(".env")

db_helper = DatabaseHelper(
    db=config.db,
    echo=config.db.echo,
)
