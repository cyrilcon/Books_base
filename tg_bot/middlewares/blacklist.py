from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class BlacklistMiddleware(BaseMiddleware):
    """
    Middleware to check if the user is blacklisted.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = data["user"]
        l10n = data["l10n"]

        if user.is_blacklisted:
            await event.answer(l10n.format_value("error-user-blacklisted"))
            return

        return await handler(event, data)
