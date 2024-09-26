from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from api.books_base_api import api


class DatabaseMiddleware(BaseMiddleware):
    """
    Middleware to handle user data in the database.

    This middleware checks if the user exists in the database.
    If the user exists, it updates their information.
    If the user does not exist, it creates a new user entry.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        id_user = event.from_user.id

        if id_user == event._bot.id:
            return await handler(event, data)

        response = await api.users.get_user_by_id(id_user)
        status = response.status

        if status == 200:
            await api.users.update_user(id_user)
        else:
            language_code = event.from_user.language_code
            full_name = event.from_user.full_name
            username = event.from_user.username

            await api.users.create_user(
                id_user,
                language_code=language_code,
                full_name=full_name,
                username=username,
            )

        return await handler(event, data)
