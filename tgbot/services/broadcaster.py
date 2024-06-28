import asyncio
import logging

from aiogram import Bot, exceptions

from tgbot.config import Config


async def send_message(
    config: Config,
    bot: Bot,
    chat_id: int,
    from_chat_id: int,
    message_id: int,
) -> bool:
    """
    Безопасное отправление сообщений.

    :param config: Config с параметрами бота.
    :param bot: Экземпляр бота.
    :param chat_id: ID пользователя.
    :param from_chat_id: ID пользователя, от которого отправляется сообщение.
    :param message_id: ID сообщения.
    :return: True/False
    """

    try:
        await bot.copy_message(chat_id, from_chat_id, message_id)
    except exceptions.TelegramBadRequest as e:
        logging.error("Telegram server says - Bad Request: chat not found")
    except exceptions.TelegramForbiddenError:
        logging.error(f"Target [ID:{chat_id}]: got TelegramForbiddenError")
    except exceptions.TelegramMigrateToChat:
        logging.error(
            f"Target [ID:{chat_id}]: group chat was upgraded to a supergroup chat"
        )
        # await delete_chat(config, user_id)  # Удаляется чат
    except exceptions.TelegramRetryAfter as e:
        logging.error(
            f"Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.retry_after} seconds."
        )
        await asyncio.sleep(e.retry_after)
        return await send_message(
            config, bot, chat_id, from_chat_id, message_id
        )  # Рекурсивный вызов
    except exceptions.TelegramAPIError:
        logging.exception(f"Target [ID:{chat_id}]: failed")
    else:
        logging.info(f"Target [ID:{chat_id}]: success")
        return True
    return False


async def broadcast(
    config: Config,
    bot: Bot,
    users: list[str | int],
    from_chat_id: int,
    message_id: int,
) -> int:
    """
    Простая рассылка.

    :param config: Config с параметрами бота.
    :param bot: Экземпляр бота.
    :param users: Список пользователей.
    :param from_chat_id: ID пользователя, от которого отправляется сообщение.
    :param message_id: ID сообщения.
    :return: К-во отправленных сообщений.
    """

    count = 0
    try:
        for chat_id in users:
            if await send_message(config, bot, chat_id, from_chat_id, message_id):
                count += 1
            await asyncio.sleep(
                0.05
            )  # 20 сообщений в секунду (Ограничение: 30 сообщений в секунду)
    finally:
        logging.info(f"{count} messages successful sent.")

    return count
