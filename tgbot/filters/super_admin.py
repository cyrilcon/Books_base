from aiogram.filters import BaseFilter
from aiogram.types import Message

from tgbot.config import config


class SuperAdminFilter(BaseFilter):
    """
    A filter to authenticate a super admin.
    """

    def __init__(self):
        self.is_super_admin: bool = True

    async def __call__(self, message: Message) -> bool:
        super_admin = config.tg_bot.super_admin
        return (message.from_user.id == super_admin) == self.is_super_admin
