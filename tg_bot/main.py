import asyncio
import logging

import betterlogging as bl
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.exceptions import AiogramError
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.fsm.strategy import FSMStrategy

from api.books_base_api import api
from config import config
from handlers import routers
from middlewares import (
    ClearKeyboardMiddleware,
    DatabaseMiddleware,
    LocalizationMiddleware,
    StorageMiddleware,
    ThrottlingMiddleware,
)
from services import set_default_commands


async def on_startup(bot: Bot):
    """
    Called on bot startup.
    """

    response = await api.users.admins.get_admin_ids()
    admins = response.result

    await set_default_commands(bot, admins)
    for admin in admins:
        try:
            await bot.send_message(chat_id=admin, text="Bot restarted!!")
        except AiogramError:
            pass


async def on_shutdown():
    """
    Called on bot shutdown.
    """

    await api.close()


def register_global_middlewares(dp: Dispatcher, storage: RedisStorage):
    """
    Register global middlewares for the given dispatcher.

    :param dp: The dispatcher instance.
    :type dp: Dispatcher
    :param storage: Storage for FSM.
    :type storage: RedisStorage
    :return: None
    """

    middleware_types = [
        ClearKeyboardMiddleware(storage),
        DatabaseMiddleware(),
        LocalizationMiddleware(),
        StorageMiddleware(storage),
        ThrottlingMiddleware(storage, throttle_time=60),
    ]

    for middleware_type in middleware_types:
        # dp.message.outer_middleware(middleware_type)
        # dp.callback_query.outer_middleware(middleware_type)
        dp.message.middleware(middleware_type)
        dp.callback_query.middleware(middleware_type)


def setup_logging():
    """
    Set up logging configuration for the application.
    """

    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=config.logging_level,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting the bot")


def get_storage():
    """
    Return storage based on the provided configuration.

    Returns:
        Storage: The storage object based on the configuration.
    """

    if config.use_redis:
        return RedisStorage.from_url(
            config.redis.dsn(),
            key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
        )
    else:
        return MemoryStorage()


async def main():
    setup_logging()  # Set logging

    storage = get_storage()

    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    dp = Dispatcher(
        storage=storage,
        fsm_strategy=FSMStrategy.CHAT,  # CHAT - state and data common for the whole chat
    )

    dp.include_routers(routers)  # Installing routers

    register_global_middlewares(dp, storage)  # Installing middlewares

    await on_startup(bot)
    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Stopping the bot")
