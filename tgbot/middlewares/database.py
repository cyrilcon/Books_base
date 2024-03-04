from datetime import datetime
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery

from infrastructure.database.repo.requests import RequestsRepo


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session_pool) -> None:
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            repo = RequestsRepo(session)

            if isinstance(event, CallbackQuery):
                chat_id = event.message.chat.id
            else:
                chat_id = event.chat.id

            user = await repo.users.user_activity(
                chat_id,
                datetime.now(),
            )  # В user содержится строка <Chat_Group_Telegram 1657591024 None 2024-01-14 20:54:21.729147 None>

            data["session"] = session
            data["repo"] = repo
            data["user"] = user

        result = await handler(event, data)  # print(await handler(event, data))
        return result
