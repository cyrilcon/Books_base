from aiogram.filters import BaseFilter
from aiogram.types import Message

from infrastructure.books_base_api import api


class AdminFilter(BaseFilter):
    """
    A filter to authenticate an admin.
    """

    def __init__(self):
        self.is_admin: bool = True

    async def __call__(self, message: Message) -> bool:
        response = await api.admins.get_admin_ids()
        admins = response.result

        return (message.from_user.id in admins) == self.is_admin
