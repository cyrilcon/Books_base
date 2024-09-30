from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from api.books_base_api import api


class BlacklistMiddleware(BaseMiddleware):
    """
    Middleware to check if the user is blacklisted.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        id_user = event.from_user.id
        l10n = data["l10n"]

        # Проверяем, является ли сообщение от бота
        if id_user == event._bot.id:
            return await handler(event, data)

        # Получаем информацию о пользователе
        response = await api.users.get_user_by_id(id_user=id_user)
        user = response.get_model()

        # Если пользователь в черном списке, отправляем сообщение и прекращаем обработку
        if user.is_blacklisted:
            await event.answer(l10n.format_value("error-user-blacklisted"))
            return  # Прекращаем выполнение обработчиков

        # Если пользователь не в черном списке, продолжаем обработку
        return await handler(event, data)
