import re

from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery

from tgbot.filters.private_chat import IsPrivate
from tgbot.services import process_search

search_title_router = Router()
search_title_router.message.filter(IsPrivate())


@search_title_router.message(F.text, StateFilter(None))
async def search_echo(message: types.Message):
    """
    Поиск книги по названию.
    :param message: Название книги, которую ищет пользователь.
    """

    await process_search(message, 1)


@search_title_router.callback_query(F.data.startswith("page"))
async def search_flipping(call: CallbackQuery):
    """
    Обработка кнопок вперёд и назад для поиска.
    :param call: Кнопка вперёд или назад.
    :return: Следующую/предыдущую страницу поиска.
    """

    await call.answer(cache_time=1)

    title_from_message = re.findall(r'"([^"]*)"', call.message.text)[0]
    page = int(call.data.split(":")[-1])

    await process_search(call.message, page, title_from_message)
