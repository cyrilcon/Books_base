import asyncio
import logging
from typing import Union

from aiogram import Bot, exceptions
from aiogram.types import InlineKeyboardMarkup

from tgbot.config import Config


async def send_message(
    config: Config,
    bot: Bot,
    id_user: Union[int, str],
    text: str,
    photo: str = None,
    disable_notification: bool = False,
    reply_markup: InlineKeyboardMarkup = None,
) -> bool:
    """
    Безопасное отправление сообщений.

    :param config: Config с параметрами бота.
    :param bot: Экземпляр бота.
    :param id_user: ID пользователя. Если str - должно содержать только цифры.
    :param text: Текст сообщения.
    :param photo: ID фото.
    :param disable_notification: Отключать уведомление или нет.
    :param reply_markup: Объект клавиатуры.
    :return: True/False
    """

    try:
        if photo:
            await bot.send_photo(
                id_user,
                photo=photo,
                caption=text,
                disable_notification=disable_notification,
                reply_markup=reply_markup,
            )
        else:
            await bot.send_message(
                id_user,
                text,
                disable_notification=disable_notification,
                reply_markup=reply_markup,
            )
    except exceptions.TelegramBadRequest as e:
        logging.error("Telegram server says - Bad Request: chat not found")
    except exceptions.TelegramForbiddenError:
        logging.error(f"Target [ID:{id_user}]: got TelegramForbiddenError")
    except exceptions.TelegramMigrateToChat:
        logging.error(
            f"Target [ID:{id_user}]: group chat was upgraded to a supergroup chat"
        )
        # await delete_chat(config, user_id)  # Удаляется чат
    except exceptions.TelegramRetryAfter as e:
        logging.error(
            f"Target [ID:{id_user}]: Flood limit is exceeded. Sleep {e.retry_after} seconds."
        )
        await asyncio.sleep(e.retry_after)
        return await send_message(
            config, bot, id_user, text, photo, disable_notification, reply_markup
        )  # Рекурсивный вызов
    except exceptions.TelegramAPIError:
        logging.exception(f"Target [ID:{id_user}]: failed")
    else:
        logging.info(f"Target [ID:{id_user}]: success")
        return True
    return False


async def broadcast(
    config: Config,
    bot: Bot,
    users: list[Union[str, int]],
    text: str,
    photo: str = None,
    disable_notification: bool = False,
    reply_markup: InlineKeyboardMarkup = None,
) -> int:
    """
    Простая рассылка.

    :param config: Config с параметрами бота.
    :param bot: Экземпляр бота.
    :param users: Список пользователей.
    :param text: Текст сообщения.
    :param photo: ID фото.
    :param disable_notification: Отключать уведомление или нет.
    :param reply_markup: Объект клавиатуры.
    :return: К-во отправленных сообщений.
    """

    count = 0
    try:
        for user_id in users:
            if await send_message(
                config, bot, user_id, text, photo, disable_notification, reply_markup
            ):
                count += 1
            await asyncio.sleep(
                0.05
            )  # 20 сообщений в секунду (Ограничение: 30 сообщений в секунду)
    finally:
        logging.info(f"{count} messages successful sent.")

    return count
