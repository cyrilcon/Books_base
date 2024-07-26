from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message


class ClearKeyboardMiddleware(BaseMiddleware):
    """
    Middleware for removing inline keyboard from the previous user's message.

    This middleware checks if the user has a previous message with inline buttons,
    and removes them before processing a new message. After handling the message,
    the middleware saves the ID of the current message with inline buttons in Redis for future reference.

    :param storage: RedisStorage object used for storing message IDs.
    """

    def __init__(self, storage: RedisStorage):
        self.storage = storage

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id
        previous_message_id = await self.storage.redis.get(f"last_message_id:{user_id}")

        if previous_message_id:
            try:
                await data["bot"].edit_message_reply_markup(
                    chat_id=event.chat.id,
                    message_id=previous_message_id,
                    reply_markup=None,
                )
            except Exception:
                pass

        result = await handler(event, data)

        state: FSMContext = data["state"]
        data = await state.get_data()
        sent_message_id = data.get("sent_message_id")

        if sent_message_id:
            await self.storage.redis.set(f"last_message_id:{user_id}", sent_message_id)

        return result
