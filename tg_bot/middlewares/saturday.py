from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject
from datetime import datetime

from fluent.runtime import FluentLocalization


class SaturdayMiddleware(BaseMiddleware):
    """
    Middleware to check that today is Saturday.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        l10n: FluentLocalization = data["l10n"]
        state: FSMContext = data["state"]

        current_day = datetime.now().weekday()

        if current_day == 5:
            await event.answer(l10n.format_value("saturday-error"))
            await state.clear()
            return

        return await handler(event, data)
