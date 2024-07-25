# from typing import Any, Awaitable, Callable, Dict, List
#
# from aiogram import BaseMiddleware
# from aiogram.fsm.storage.redis import RedisStorage
# from aiogram.types import Message, TelegramObject
#
#
# class ThrottlingMiddleware(BaseMiddleware):
#     def __init__(
#         self, storage: RedisStorage, time_throttling: int, throttled_commands: List[str]
#     ):
#         self.storage = storage  # Объект хранилища Redis
#         self.time_throttling = time_throttling  # Время троттлинла
#         self.throttled_commands = (
#             throttled_commands  # Команды и фразы, которые нужно троттлить
#         )
#
#     async def __call__(
#         self,
#         handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
#         event: Message,
#         data: Dict[str, Any],
#     ) -> Any:
#         if isinstance(event, Message) and event.text in self.throttled_commands:
#             user = f"user_{event.from_user.id}"
#             check_user = await self.storage.redis.get(name=user)
#
#             if check_user:
#                 time_left = await self.storage.redis.ttl(
#                     name=user
#                 )  # Оставшееся время жизни ключа
#                 if int(check_user.decode()) == 1:  # Попадает под спам фильтр
#                     await self.storage.redis.set(name=user, value=0, ex=time_left)
#                     return await event.answer(
#                         f"Слишком частый запрос, повторите через <b>{time_left}</b> секунд"
#                     )
#                 return
#
#             await self.storage.redis.set(name=user, value=1, ex=self.time_throttling)
#             return await handler(event, data)
#
#         # Если сообщение не являлось командой из списка, пропуск обработки без троттлинга
#         return await handler(event, data)
