import asyncio
import logging

from aiogram import Bot, exceptions
from aiogram.types import InlineKeyboardMarkup


class Messenger:
    @staticmethod
    async def safe_send_message(
        bot: Bot,
        user_id: int,
        text: str,
        photo: str = None,
        disable_notification: bool = False,
        reply_markup: InlineKeyboardMarkup = None,
    ) -> bool:
        """
        Safe message sender.
        :param bot: Bot instance.
        :param user_id: User id.
        :param text: Text of the message.
        :param photo: Photo attached to the message.
        :param disable_notification: Disable notification or not.
        :param reply_markup: Reply markup.
        :return: Success.
        """

        try:
            if photo:
                await bot.send_photo(
                    user_id,
                    photo=photo,
                    caption=text,
                    disable_notification=disable_notification,
                    reply_markup=reply_markup,
                )
            else:
                await bot.send_message(
                    user_id,
                    text,
                    disable_notification=disable_notification,
                    reply_markup=reply_markup,
                )
        except exceptions.TelegramBadRequest as e:
            logging.error("Telegram server says - Bad Request: chat not found")
        except exceptions.TelegramForbiddenError:
            logging.error(f"Target [ID:{user_id}]: got TelegramForbiddenError")
        except exceptions.TelegramMigrateToChat:
            logging.error(
                f"Target [ID:{user_id}]: group chat was upgraded to a supergroup chat"
            )
        except exceptions.TelegramRetryAfter as e:
            logging.error(
                f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.retry_after} seconds."
            )
            await asyncio.sleep(e.retry_after)
            return await Messenger.safe_send_message(
                bot, user_id, text, photo, disable_notification, reply_markup
            )  # Recursive call
        except exceptions.TelegramAPIError:
            logging.exception(f"Target [ID:{user_id}]: failed")
        else:
            logging.info(f"Target [ID:{user_id}]: success")
            return True
        return False

    @staticmethod
    async def safe_broadcast(
        bot: Bot,
        users: list[int],
        text: str,
        photo: str = None,
        disable_notification: bool = False,
        reply_markup: InlineKeyboardMarkup = None,
    ) -> int:
        """
        Simple broadcaster.
        :param bot: Bot instance.
        :param users: List of users.
        :param text: Text of the message.
        :param photo: Photo attached to the message.
        :param disable_notification: Disable notification or not.
        :param reply_markup: Reply markup.
        :return: Count of messages.
        """

        count = 0
        try:
            for user_id in users:
                if await Messenger.safe_send_message(
                    bot, user_id, text, photo, disable_notification, reply_markup
                ):
                    count += 1
                await asyncio.sleep(
                    0.05
                )  # 20 messages per second (Limit: 30 messages per second)
        finally:
            logging.info(f"{count} messages successful sent.")

        return count
