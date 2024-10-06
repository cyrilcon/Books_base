from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from api.books_base_api.schemas import UserSchema
from tg_bot.services import get_fluent_localization


class LocalizationMiddleware(BaseMiddleware):
    """
    Middleware to retrieve and inject the user's preferred language for localization purposes.
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

        user: UserSchema = data["user"]

        l10n = get_fluent_localization(user.language_code)
        data["l10n"] = l10n

        return await handler(event, data)
