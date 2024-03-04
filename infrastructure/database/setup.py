from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from tgbot.config import DbConfig


def create_engine(db: DbConfig, echo=True):
    engine = create_async_engine(
        db.construct_sqlalchemy_url(),
        query_cache_size=1200,  # Устанавливает размер кэша запросов (2400)
        pool_size=1000,  # Устанавливает максимальное количество соединений в пуле (150)
        # max_overflow устанавливает максимальное количество соединений,
        # которые могут быть созданы поверх установленного pool_size (500)
        max_overflow=4000,
        future=True,  # Включает использование объектов FutureResult для асинхронных запросов.
        echo=echo,  # Управляет выводом SQL-запросов в консоль для отладки.
    )
    return engine


def create_session_pool(engine):
    session_pool = async_sessionmaker(bind=engine, expire_on_commit=False)
    return session_pool
