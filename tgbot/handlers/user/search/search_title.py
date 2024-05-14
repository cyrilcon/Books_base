import re

from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery

from tgbot.filters.private_chat import IsPrivate
from tgbot.services import process_search, get_user_language

search_title_router = Router()
search_title_router.message.filter(IsPrivate())


@search_title_router.message(F.text, StateFilter(None))
async def search_echo(message: types.Message):
    """
    Поиск книги по названию.
    :param message: Название книги, которую ищет пользователь.
    """

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    await process_search(message, l10n, 1)


@search_title_router.callback_query(F.data.startswith("page"))
async def search_flipping(call: CallbackQuery):
    """
    Обработка кнопок вперёд и назад для поиска.
    :param call: Кнопка вперёд или назад.
    :return: Следующую/предыдущую страницу поиска.
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.answer(cache_time=1)

    title_from_message = re.findall(r'"([^"]*)"', call.message.text)[0]
    page = int(call.data.split(":")[-1])

    await process_search(call.message, l10n, page, title_from_message)
