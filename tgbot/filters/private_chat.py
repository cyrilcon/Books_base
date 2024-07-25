from aiogram.filters import BaseFilter
from aiogram.types import Message

from tgbot.config import Config


class IsPrivate(BaseFilter):
    """
    A filter to check the privacy of a chat room.

    Attributes
    ----------
    :param is_private: Check if the chat is private.
    :type is_private: bool
    :return: True/False
    """

    is_private: str = "private"

    async def __call__(self, obj: Message, config: Config) -> bool:
        return obj.chat.type == self.is_private
