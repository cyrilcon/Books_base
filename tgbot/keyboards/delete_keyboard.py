from aiogram import Bot
from aiogram.exceptions import TelegramNotFound, TelegramBadRequest, TelegramForbiddenError
from aiogram.types import Message


async def delete_keyboard(bot: Bot, message: Message):
    """
    Удаляется inline клавиатуру из предыдущего сообщения бота.
    :param bot: Экземпляр бота.
    :param message: Сообщение, у которого нужно удалить inline клавиатуру.
    :return: Убирается inline клавиатура.
    """

    message_id = message.message_id
    try:
        await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message_id - 1, reply_markup=None)
    except (TelegramNotFound, TelegramBadRequest, TelegramForbiddenError):
        pass
