from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from infrastructure.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import cancel_keyboard
from tgbot.services import find_user, create_user_link
from tgbot.states import AddAdmin

add_admin_router = Router()
add_admin_router.message.filter(AdminFilter())


@add_admin_router.message(Command("add_admin"))
async def add_admin(message: Message, l10n: FluentLocalization, state: FSMContext):
    """
    Processing of the /add_admin command.
    :param message: /add_admin command.
    :param l10n: Language set by the user.
    :param state: FSM (AddAdmin).
    :return: Message to add a user to the admin list and go to FSM (AddAdmin).
    """

    sent_message = await message.answer(
        l10n.format_value("add-admin-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(AddAdmin.select_user)
    await state.update_data(new_message_id=sent_message.message_id)


@add_admin_router.message(StateFilter(AddAdmin.select_user))
async def add_admin_process(
    message: Message, l10n: FluentLocalization, state: FSMContext
):
    """
    Selects the user to add to the admin list.
    :param message: A message with the expected username or user ID.
    :param l10n: Language set by the user.
    :param state: FSM (AddAdmin).
    :return: Adding a user to the blacklist.
    """

    user, response_message = await find_user(message.text, l10n)

    if user:
        id_user = user["id_user"]
        fullname = user["fullname"]
        username = user["username"]
        url_user = await create_user_link(fullname, username)

        response = await api.admins.create_admin(id_user)
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
            sent_message = await message.answer(
                l10n.format_value(
                    "add-admin-error",
                    {"url_user": url_user, "id_user": str(id_user)},
                ),
                reply_markup=cancel_keyboard(l10n),
            )
            await state.update_data(new_message_id=sent_message.message_id)
    else:
        sent_message = await message.answer(
            response_message, reply_markup=cancel_keyboard(l10n)
        )
        await state.update_data(new_message_id=sent_message.message_id)
