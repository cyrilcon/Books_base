from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message


class ConfigMiddleware(BaseMiddleware):
    """
    Middleware для получения данных config о боте.
    Пример:
    Config(tg_bot=TgBot(token='6615153332:AAF8-eU-eEFVmIh5tnxCqtVg93piHOpAeB0', admins=[1657591024], use_redis=True),
    db=DbConfig(host='localhost', password='alcohol', user='testuser', database='test', port=5432),
    redis=RedisConfig(redis_pass='temnomor', redis_port=6388, redis_host='localhost'))
    """

    def __init__(self, config) -> None:
        self.config = config

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        data["config"] = self.config
        return await handler(event, data)  # print(await handler(event, data))
