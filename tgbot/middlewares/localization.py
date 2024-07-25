from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from tgbot.services import get_user_language


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
        l10n = await get_user_language(id_user)
        data["l10n"] = l10n
        return await handler(event, data)
