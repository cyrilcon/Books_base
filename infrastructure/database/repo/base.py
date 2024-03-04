from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepo:
    """
    Класс, представляющий базовое хранилище для обработки операций с базой данных.

    Attributes:
        session (AsyncSession): Сессия базы данных, используемая хранилищем.
    """

    def __init__(self, session):
        self.session: AsyncSession = session
