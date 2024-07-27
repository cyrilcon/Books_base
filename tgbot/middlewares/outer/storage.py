from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class StorageMiddleware(BaseMiddleware):
    """
    Middleware to retrieve storage.
    """

    def __init__(self, storage) -> None:
        self.storage = storage

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["storage"] = self.storage
        return await handler(event, data)
