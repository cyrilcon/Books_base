import re

from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter, CommandObject
from aiogram.types import Message

from infrastructure.books_base_api import api
from tgbot.services import get_fluent_localization
from tgbot.states import all_states

start_router = Router()


@start_router.message(
    CommandStart(deep_link=True, magic=F.args.regexp(re.compile(r"book_(\d+)")))
)
async def cmd_start_book(message: Message, command: CommandObject):
    book_number = command.args.split("_")[1]
    await message.answer(f"Sending book №{book_number}")


@start_router.message(CommandStart())
@start_router.message(StateFilter(all_states))
async def start(message: Message):
    """
    Обработка команды /start.
    :param message: Команда /start.
    :return: Сообщение приветствие бота.
    """

    id_user = message.from_user.id
    fullname = message.from_user.full_name
    username = message.from_user.username

    status, user = await api.users.get_user(id_user)
    if status == 404:
        language = message.from_user.language_code
        await api.users.add_user(id_user, language, fullname, username)
    else:
        language = user["language"]
        await api.users.update_user(id_user, fullname=fullname, username=username)

    l10n = get_fluent_localization(language)
    text = f", <b>{fullname}</b>" if fullname else None
    await message.answer(l10n.format_value("start-text", {"additional_text": text}))
