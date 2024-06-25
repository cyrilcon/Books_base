import re

from aiogram import Router, types, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery

from tgbot.config import Config
from tgbot.filters import IsPrivate
from tgbot.services import process_search

search_title_router = Router()
search_title_router.message.filter(IsPrivate())


@search_title_router.message(F.text, StateFilter(None))
async def search_echo(message: types.Message, bot: Bot, config: Config):
    """
    Поиск книги по названию.
    :param message: Название книги, которую ищет пользователь.
    :param bot: Экземпляр бота.
    :param config: Config с параметрами бота.
    """

    id_user = message.from_user.id

    await process_search(config, bot, id_user, message, 1)


@search_title_router.callback_query(F.data.startswith("page"))
async def search_flipping(call: CallbackQuery, bot: Bot, config: Config):
    """
    Обработка кнопок вперёд и назад для поиска.
    :param call: Кнопка вперёд или назад.
    :param bot: Экземпляр бота.
    :param config: Config с параметрами бота.
    :return: Следующую/предыдущую страницу поиска.
    """

    id_user = call.from_user.id

    await call.answer(cache_time=1)

    # title_from_message = re.findall(r'"([^"]*)"', call.message.text)[0]
    title_from_message = re.search(r'"([^"]*)"', call.message.text).group(1)
    page = int(call.data.split(":")[-1])

    await process_search(config, bot, id_user, call.message, page, title_from_message)
