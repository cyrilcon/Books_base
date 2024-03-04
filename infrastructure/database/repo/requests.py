from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.models.base import Base
from infrastructure.database.repo.users import UserRepo
from infrastructure.database.setup import create_engine
from tgbot.config import Config


@dataclass
class RequestsRepo:
    """
    Репозиторий для обработки операций с базами данных. В этом классе хранятся все репозитории для моделей баз данных.
    """

    session: AsyncSession

    @property
    def users(self) -> UserRepo:
        """
        Репозиторий для работы с пользователем.
        """

        return UserRepo(self.session)


async def create_tables(config: Config):
    """
    Создание таблицы в базе данных.
    :param config: Объект конфигурации, загруженный из конфигурации бота.
    """

    engine = create_engine(config.db)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
