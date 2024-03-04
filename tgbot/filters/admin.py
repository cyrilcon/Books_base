from aiogram.filters import BaseFilter
from aiogram.types import Message

from tgbot.config import Config


class AdminFilter(BaseFilter):
    """
    Фильтр для проверки подлинности админа.

    Атрибуты
    ----------
    :param is_admin: Проверка подлинности админа.
    :type is_admin: Bool.
    :return: True/False
    """

    is_admin: bool = True

    async def __call__(self, obj: Message, config: Config) -> bool:
        return (obj.from_user.id in config.tg_bot.admins) == self.is_admin
