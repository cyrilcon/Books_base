from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from infrastructure.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import cancel_keyboard
from tgbot.services import get_user_language, check_username, get_url_user
from tgbot.states import AddToBlacklist

add_to_blacklist_router = Router()
add_to_blacklist_router.message.filter(AdminFilter())


@add_to_blacklist_router.message(Command("add_to_blacklist"))
async def add_to_blacklist(message: Message, state: FSMContext):
    """
    Обработка команды /add_to_blacklist.
    :param message: Команда /add_to_blacklist.
    :param state: FSM (AddToBlacklist).
    :return: Сообщение для добавления пользователя в чёрный список и переход в FSM (AddToBlacklist).
    """

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    await message.answer(
        l10n.format_value("add-to-blacklist-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )

    await state.set_state(AddToBlacklist.select_user)


@add_to_blacklist_router.message(StateFilter(AddToBlacklist.select_user))
async def add_to_blacklist_process(message: Message, bot: Bot, state: FSMContext):
    """
    Выбор пользователя для добавления его в чёрный список.
    :param message: Сообщение с ожидаемым именем пользователя или его ID.
    :param bot: Экземпляр бота.
    :param state: FSM (AddToBlacklist).
    :return: Добавление пользователя в чёрный список.
    """

    await delete_keyboard(bot, message)

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    message_text = message.text

    if message_text.isdigit():
        id_user = int(message_text)

        response = await api.users.get_user(id_user)
        status = response.status

        if status == 200:
            await user_found(id_user, message, l10n, state)
        else:
            await message.answer(
                l10n.format_value("user-not-found-by-id", {"id_user": str(id_user)}),
                reply_markup=cancel_keyboard(l10n),
            )
    else:
        selected_user = check_username(message_text)

        if selected_user:
            response = await api.users.get_user_by_username(selected_user)
            status = response.status

            if status == 200:
                await user_found(id_user, message, l10n, state)
            else:
                await message.answer(
                    l10n.format_value(
                        "user-not-found-by-username", {"username": selected_user}
                    ),
                    reply_markup=cancel_keyboard(l10n),
                )
        else:
            await message.answer(
                l10n.format_value("username-incorrect"),
                reply_markup=cancel_keyboard(l10n),
            )


async def user_found(id_user, message, l10n, state):
    """
    Сценарий, если пользователь найден.
    :param id_user: ID пользователя.
    :param message: Сообщение с ожидаемым именем пользователя или его ID.
    :param l10n: Язык установленный у пользователя.
    :param state: Класс состояний.
    :return: Добавление пользователя в чёрный список.
    """

    await api.users.add_to_blacklist(id_user)

    response = await api.users.get_user(id_user)
    user = response.result
    fullname = user["fullname"]
    username = user["username"]

    url_user = await get_url_user(fullname, username)

    text = "add-to-blacklist-user-was-added"

    await message.answer(
        l10n.format_value(text, {"url_user": url_user, "id_user": str(id_user)}),
    )

    await state.clear()
