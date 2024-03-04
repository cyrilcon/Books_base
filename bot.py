import asyncio
import logging

import betterlogging as bl
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.fsm.strategy import FSMStrategy

from infrastructure.database.repo.requests import create_tables
from infrastructure.database.setup import create_engine, create_session_pool
from tgbot.config import load_config, Config
from tgbot.handlers import routers_list
from tgbot.middlewares import ConfigMiddleware
from tgbot.services import set_default_commands, broadcaster


async def on_startup(config: Config, bot: Bot, admins: list[int]):
    """
    Вызывается при старте бота.
    Установка команд из меню бота и уведомление админов о запуске бота.
    """

    await set_default_commands(bot)  # Команды из меню бота
    await broadcaster.broadcast(config, bot, admins, "Бот перезапущен!!")  # Уведомление админов о запуске бота


def register_global_middlewares(dp: Dispatcher, config: Config):
    """
    Регистрация глобальных мидлварей.

    :param dp: Экземпляр диспатчера.
    :type dp: Dispatcher.
    :param config: Объект конфигурации из загруженного конфига.
    :type config: Config.
    :return: None
    """

    middleware_types = [
        ConfigMiddleware(config),
        # DatabaseMiddleware(session_pool),
    ]

    for middleware_type in middleware_types:
        dp.message.outer_middleware(middleware_type)
        dp.callback_query.outer_middleware(middleware_type)


def setup_logging():
    """
    Настройка логирования.
    """

    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting the bot")


def get_storage(config):
    """
    Выбор хранилища на основе конфигурации.

    Args:
        config (Config): Объект конфигурации.

    Returns:
        Storage: Объект хранения на основе конфигурации.
    """

    if config.tg_bot.use_redis:
        return RedisStorage.from_url(
            config.redis.dsn(),
            key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
        )
    else:
        return MemoryStorage()


async def main():
    setup_logging()  # Установка логирования

    config = load_config(".env")
    storage = get_storage(config)

    # engine = create_engine(config.db)
    # session_pool = create_session_pool(engine)
    #
    # await create_tables(config)  # Создание таблицы в бд

    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=storage, fsm_strategy=FSMStrategy.CHAT)  # CHAT — стейт и данные общие для всего чата.
    # В ЛС разница незаметна, но в группе у всех участников будет один стейт и общие данные.

    dp.include_routers(*routers_list)  # Установка роутеров

    register_global_middlewares(dp, config)  # Установка мидлварей

    # Установка команд из меню бота и уведомление админов о запуске бота
    await on_startup(config, bot, config.tg_bot.admins)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Stopping the bot")
