import time
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import TelegramObject
from fluent.runtime import FluentLocalization


class ThrottlingMiddleware(BaseMiddleware):
    """
    Middleware for trotting commands and keystrokes.
    """

    def __init__(self, storage: RedisStorage, throttle_time: int):
        self.storage = storage
        self.throttle_time = throttle_time

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        l10n: FluentLocalization = data["l10n"]
        user_id = event.from_user.id

        throttling_enabled = get_flag(data, "throttle", default=False)

        if not throttling_enabled:
            return await handler(event, data)

        user_key = f"throttle_{user_id}"

        last_request_time = await self.storage.redis.get(user_key)

        if last_request_time:
            time_left = self.throttle_time - (time.time() - float(last_request_time))

            if time_left > 0:
                await event.answer(
                    l10n.format_value(
                        "throttling",
                        {"time_left": int(time_left)},
                    )
                )
                return

        await self.storage.redis.set(user_key, str(time.time()), ex=self.throttle_time)
        return await handler(event, data)
