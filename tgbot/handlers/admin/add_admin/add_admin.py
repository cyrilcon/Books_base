from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from infrastructure.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import cancel_keyboard
from tgbot.services import get_user_language, find_user, get_url_user
from tgbot.states import AddAdmin

add_admin_router = Router()
add_admin_router.message.filter(AdminFilter())


@add_admin_router.message(Command("add_admin"))
async def add_admin(message: Message, state: FSMContext):
    """
    Обработка команды /add_admin.
    :param message: Команда /add_admin.
    :param state: FSM (AddAdmin).
    :return: Сообщение для добавления пользователя в список админов и переход в FSM (AddAdmin).
    """

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    await message.answer(
        l10n.format_value("add-admin-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )

    await state.set_state(AddAdmin.select_user)


@add_admin_router.message(StateFilter(AddAdmin.select_user))
async def add_admin_process(message: Message, bot: Bot, state: FSMContext):
    """
    Выбор пользователя для добавления его в список администраторов.
    :param message: Сообщение с ожидаемым именем пользователя или его ID.
    :param bot: Экземпляр бота.
    :param state: FSM (AddAdmin).
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

        response = await api.users.add_admin(id_user)
        status = response.status

        if status == 201:
            await message.answer(
                l10n.format_value(
                    "add-admin-was-added",
                    {"url_user": url_user, "id_user": str(id_user)},
                )
            )
            await state.clear()
        else:
            await message.answer(
                l10n.format_value(
                    "add-admin-user-is-already-admin",
                    {"url_user": url_user, "id_user": str(id_user)},
                ),
                reply_markup=cancel_keyboard(l10n),
            )
    else:
        await message.answer(response_message, reply_markup=cancel_keyboard(l10n))
