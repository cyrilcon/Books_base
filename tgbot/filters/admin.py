from aiogram.filters import BaseFilter
from aiogram.types import Message

from infrastructure.books_base_api import api
from tgbot.config import Config


class AdminFilter(BaseFilter):
    """
    A filter to authenticate an admin.

    Attributes
    ----------
    :param is_admin: Admin authentication.
    :type is_admin: bool
    :return: True/False
    """

    is_admin: bool = True

    async def __call__(self, obj: Message, config: Config) -> bool:
        response = await api.users.get_admins()
        admins = response.result

        return (obj.from_user.id in admins) == self.is_admin
