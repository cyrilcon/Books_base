from aiogram.filters import BaseFilter
from aiogram.types import Message

from tgbot.config import Config


class IsPrivate(BaseFilter):
    """
    Фильтр на проверку приватности чата.

    Атрибуты
    ----------
    :param is_private: Проверка приватности чата.
    :type is_private: Bool.
    :return: True/False
    """

    is_private: str = 'private'

    async def __call__(self, obj: Message, config: Config) -> bool:
        return obj.chat.type == self.is_private
