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
        full_name = event.from_user.full_name
        username = event.from_user.username

        response = await api.users.get_user_by_id(id_user)
        status = response.status

        if status == 200:
            response = await api.users.update_user(
                id_user=id_user,
                full_name=full_name,
                username=username,
            )
        else:
            language_code = event.from_user.language_code
            response = await api.users.create_user(
                id_user,
                language_code=language_code,
                full_name=full_name,
                username=username,
            )

        user = response.get_model()
        data["user"] = user

        return await handler(event, data)
