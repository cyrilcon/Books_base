from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject
from fluent.runtime import FluentLocalization

from api.api_v1.schemas import UserSchema


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
        user: UserSchema = data["user"]
        l10n: FluentLocalization = data["l10n"]
        state: FSMContext = data["state"]

        if user.is_blacklisted:
            await event.answer(l10n.format_value("error-user-blacklisted"))
            await state.clear()
            return

        return await handler(event, data)
