from datetime import datetime
from typing import Optional

from sqlalchemy import select, update, func, delete
from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models import Telegram_Chat
from infrastructure.database.repo.base import BaseRepo


class UserRepo(BaseRepo):
    async def user_activity(
            self,
            id_chat: int,
            activity: Optional[datetime],
    ):
        """
        Добавляется чат или обновляется время активности.
        :param id_chat: ID чата.
        :param activity: Время последнего использования бота.
        :return: Объект пользователя, None, если при совершении транзакции произошла ошибка.
        """

        insert_stmt = (
            insert(Telegram_Chat)
            .values(
                id_chat=id_chat,
                activity=activity,
            )
            .on_conflict_do_update(
                index_elements=[Telegram_Chat.id_chat],
                set_=dict(
                    activity=activity
                ),
            )
            .returning(Telegram_Chat)
        )
        result = await self.session.execute(insert_stmt)

        await self.session.commit()
        return result.scalar_one()
