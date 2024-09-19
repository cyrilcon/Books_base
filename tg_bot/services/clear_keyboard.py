from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery


class ClearKeyboard:
    @staticmethod
    async def clear(message: Message | CallbackQuery, storage: RedisStorage):
        """
        Removing inline keyboard from the previous user's message.
        """
        id_user = message.from_user.id
        previous_message_id = await storage.redis.get(f"last_message_id:{id_user}")

        if previous_message_id:
            try:
                if isinstance(message, CallbackQuery):
                    message = message.message
                await message.bot.edit_message_reply_markup(
                    chat_id=message.chat.id,
                    message_id=previous_message_id,
                    reply_markup=None,
                )
            except Exception:
                pass

        await storage.redis.delete(f"last_message_id:{id_user}")

    @staticmethod
    async def safe_message(storage: RedisStorage, id_user: int, sent_message_id: int):
        """
        Saving a message that will have the inline keyboard removed.
        """
        await storage.redis.set(f"last_message_id:{id_user}", sent_message_id)
