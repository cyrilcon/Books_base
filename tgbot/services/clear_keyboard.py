from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message


class ClearKeyboard:
    @staticmethod
    async def clear(message: Message, storage: RedisStorage):
        """
        Removing inline keyboard from the previous user's message.
        """
        user_id = message.from_user.id
        previous_message_id = await storage.redis.get(f"last_message_id:{user_id}")

        if previous_message_id:
            try:
                await message.bot.edit_message_reply_markup(
                    chat_id=message.chat.id,
                    message_id=previous_message_id,
                    reply_markup=None,
                )
            except Exception:
                pass

        await storage.redis.delete(f"last_message_id:{user_id}")

    @staticmethod
    async def safe_message(storage: RedisStorage, user_id: int, sent_message_id: int):
        """
        Saving a message that will have the inline keyboard removed.
        """
        await storage.redis.set(f"last_message_id:{user_id}", sent_message_id)
