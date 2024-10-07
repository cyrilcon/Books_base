from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import TelegramObject, Message, CallbackQuery
from aiogram.fsm.storage.redis import RedisStorage


class ClearKeyboardMiddleware(BaseMiddleware):
    """
    Middleware to automatically delete the inline keyboard of a previous message.
    """

    def __init__(self, storage: RedisStorage):
        super().__init__()
        self.storage = storage

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        id_user = event.from_user.id

        clear_keyboard = get_flag(data, "clear_keyboard", default=True)
        safe_message = get_flag(data, "safe_message", default=True)

        if clear_keyboard:
            await self.clear_keyboard(event, id_user)

        result = await handler(event, data)

        if safe_message:
            if isinstance(event, Message):
                message_id = event.message_id + 1
                await self.save_message_id(id_user, message_id)

        return result

    async def clear_keyboard(self, event: TelegramObject, id_user: int):
        """
        Removing the keyboard from the previous message.
        """

        previous_message_id = await self.storage.redis.get(f"last_message_id:{id_user}")

        if previous_message_id:
            try:
                if isinstance(event, CallbackQuery):
                    event = event.message
                await event.bot.edit_message_reply_markup(
                    chat_id=event.chat.id,
                    message_id=previous_message_id,
                    reply_markup=None,
                )
            except Exception:
                pass

        await self.storage.redis.delete(f"last_message_id:{id_user}")

    async def save_message_id(self, id_user: int, message_id: int):
        """
        Saves the message ID for later clearing of the inline keypad.
        """

        await self.storage.redis.set(f"last_message_id:{id_user}", message_id)
