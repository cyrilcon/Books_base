from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.models.base import Base
from infrastructure.database.repo.users import UserRepo
from infrastructure.database.setup import db_helper


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


async def create_tables():
    """
    Создание таблицы в базе данных.
    """

    async with db_helper.engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
