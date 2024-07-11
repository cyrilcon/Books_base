from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from infrastructure.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import cancel_keyboard
from tgbot.services import get_user_language, find_user, get_url_user
from tgbot.states import AddBlacklist

add_blacklist_router = Router()
add_blacklist_router.message.filter(AdminFilter())


@add_blacklist_router.message(Command("add_blacklist"))
async def add_blacklist(message: Message, state: FSMContext):
    """
    Обработка команды /add_blacklist.
    :param message: Команда /add_blacklist.
    :param state: FSM (AddBlacklist).
    :return: Сообщение для добавления пользователя в чёрный список и переход в FSM (AddBlacklist).
    """

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    await message.answer(
        l10n.format_value("add-blacklist-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )

    await state.set_state(AddBlacklist.select_user)


@add_blacklist_router.message(StateFilter(AddBlacklist.select_user))
async def add_blacklist_process(message: Message, bot: Bot, state: FSMContext):
    """
    Выбор пользователя для добавления его в чёрный список.
    :param message: Сообщение с ожидаемым именем пользователя или его ID.
    :param bot: Экземпляр бота.
    :param state: FSM (AddBlacklist).
    :return: Добавление пользователя в чёрный список.
    """

    await delete_keyboard(bot, message)

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    status, user, response_message = await find_user(message.text, l10n)

    if status == 200:
        id_user = user["id_user"]
        fullname = user["fullname"]
        username = user["username"]
        url_user = await get_url_user(fullname, username)

        await api.users.add_blacklist(id_user)

        await message.answer(
            l10n.format_value(
                "add-blacklist-user-was-added",
                {"url_user": url_user, "id_user": str(id_user)},
            )
        )
        await state.clear()
    else:
        await message.answer(response_message, reply_markup=cancel_keyboard(l10n))
