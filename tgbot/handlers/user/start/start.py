from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message
from fluent.runtime import FluentLocalization, FluentResourceLoader

from infrastructure.books_base_api import api
from tgbot.services.fluent_loader import get_fluent_localization
from tgbot.states import all_states

start_router = Router()


@start_router.message(CommandStart())
@start_router.message(StateFilter(all_states))
async def start(message: Message):
    """
    Обработка команды /start.
    :param message: Команда /start.
    :return: Сообщение приветствие бота.
    """

    id_user = message.from_user.id
    language = message.from_user.language_code
    fullname = message.from_user.full_name
    username = message.from_user.username

    l10n = get_fluent_localization(language)

    status, result = await api.users.get_user(id_user)
    if status == 404:
        await api.users.add_user(id_user, language, fullname, username)
    else:
        await api.users.update_user(id_user, fullname=fullname, username=username)

    text = f", <b>{fullname}</b>" if fullname else None
    await message.answer(l10n.format_value("start-text", {"additional_text": text}))
