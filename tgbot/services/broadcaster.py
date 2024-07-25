import asyncio
import logging

from aiogram import Bot, exceptions


async def send_message(
    bot: Bot,
    chat_id: int,
    from_chat_id: int,
    message_id: int,
) -> bool:
    """
    Safe messages sender.
    :param bot: Bot instance.
    :param chat_id: Recipient ID.
    :param from_chat_id: Sender ID.
    :param message_id: ID of the forwarded message.
    :return: Success.
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
    except exceptions.TelegramRetryAfter as e:
        logging.error(
            f"Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.retry_after} seconds."
        )
        await asyncio.sleep(e.retry_after)
        return await send_message(
            bot, chat_id, from_chat_id, message_id
        )  # Recursive call
    except exceptions.TelegramAPIError:
        logging.exception(f"Target [ID:{chat_id}]: failed")
    else:
        logging.info(f"Target [ID:{chat_id}]: success")
        return True
    return False


async def broadcast(
    bot: Bot,
    users: list[str | int],
    from_chat_id: int,
    message_id: int,
) -> int:
    """
    Simple broadcaster.
    :param bot: Bot instance.
    :param users: List of users.
    :param from_chat_id: Sender ID.
    :param message_id: ID of the forwarded message.
    :return: Count of messages.
    """

    count = 0
    try:
        for chat_id in users:
            if await send_message(bot, chat_id, from_chat_id, message_id):
                count += 1
            await asyncio.sleep(
                0.05
            )  # 20 messages per second (Limit: 30 messages per second)
    finally:
        logging.info(f"{count} messages successful sent.")

    return count
