from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization


class CancelCommandMiddleware(BaseMiddleware):
    """
    Middleware to handle the cancellation of commands.
    """

    def __init__(self, cancel_message: str):
        self.cancel_message = cancel_message

    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        if event.data == "cancel":
            state: FSMContext = data["state"]
            l10n: FluentLocalization = data["l10n"]

            text = l10n.format_value(self.cancel_message)

            await state.clear()
            await event.answer(text, show_alert=True)
            try:
                await event.message.edit_text(text)
            except TelegramBadRequest:
                await event.message.edit_reply_markup()

            return

        return await handler(event, data)
