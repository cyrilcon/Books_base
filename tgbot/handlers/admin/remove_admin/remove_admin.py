from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from infrastructure.books_base_api import api
from tgbot.filters import SuperAdminFilter
from tgbot.keyboards.inline import cancel_keyboard
from tgbot.services import find_user, create_user_link
from tgbot.states import RemoveAdmin

remove_admin_router = Router()
remove_admin_router.message.filter(SuperAdminFilter())


@remove_admin_router.message(Command("remove_admin"))
async def remove_admin(message: Message, l10n: FluentLocalization, state: FSMContext):
    """
    Processing of the /remove_admin command.
    :param message: /remove_admin command.
    :param l10n: Language set by the user.
    :param state: FSM (RemoveAdmin).
    :return: Message to demote the administrator and go to FSM (RemoveAdmin).
    """

    sent_message = await message.answer(
        l10n.format_value("remove-admin-select"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(RemoveAdmin.select_admin)
    await state.update_data(new_message_id=sent_message.message_id)


@remove_admin_router.message(StateFilter(RemoveAdmin.select_admin))
async def remove_admin_process(
    message: Message, l10n: FluentLocalization, state: FSMContext
):
    """
    Selecting an administrator for demotion.
    :param message: A message with the expected username or user ID.
    :param l10n: Language set by the user.
    :param state: FSM (RemoveAdmin).
    :return: Administrator demotion.
    """

    user, response_message = await find_user(message.text, l10n)

    if user:
        id_user = user["id_user"]

        if id_user == message.from_user.id:
            sent_message = await message.answer(
                l10n.format_value(
                    "remove-admin-error-self-remove",
                ),
                reply_markup=cancel_keyboard(l10n),
            )
            await state.update_data(new_message_id=sent_message.message_id)
        else:
            fullname = user["fullname"]
            username = user["username"]
            url_user = await create_user_link(fullname, username)

            response = await api.admins.delete_admin(id_user)
            status = response.status

            if status == 204:
                await message.answer(
                    l10n.format_value(
                        "remove-admin-was-removed",
                        {"url_user": url_user, "id_user": str(id_user)},
                    )
                )
                await state.clear()
            else:
                sent_message = await message.answer(
                    l10n.format_value(
                        "remove-admin-error-not-admin",
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
