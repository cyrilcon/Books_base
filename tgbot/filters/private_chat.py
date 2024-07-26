from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsPrivate(BaseFilter):
    """
    A filter to check the privacy of a chat room.
    """

    def __init__(self):
        self.is_private: str = "private"

    async def __call__(self, message: Message) -> bool:
        return message.chat.type == self.is_private
