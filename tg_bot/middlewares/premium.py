from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject
from fluent.runtime import FluentLocalization

from api.books_base_api.schemas import UserSchema


class PremiumMiddleware(BaseMiddleware):
    """
    Middleware to check if the user has premium.
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

        if user.is_premium:
            await event.answer(l10n.format_value("error-user-has-premium"))
            await state.clear()
            return

        return await handler(event, data)
