from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from infrastructure.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import cancel_keyboard
from tgbot.services import find_user, create_user_link
from tgbot.states import CancelPremium

cancel_premium_router = Router()
cancel_premium_router.message.filter(AdminFilter())


@cancel_premium_router.message(Command("cancel_premium"))
async def cancel_premium(message: Message, l10n: FluentLocalization, state: FSMContext):
    """
    Processing of the /cancel_premium command.
    :param message: /cancel_premium command.
    :param l10n: Language set by the user.
    :param state: FSM (CancelPremium).
    :return: Message to select the user and go to FSM (GivePremium).
    """

    sent_message = await message.answer(
        l10n.format_value("cancel-premium-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(CancelPremium.select_user)
    await state.update_data(sent_message_id=sent_message.message_id)


@cancel_premium_router.message(StateFilter(CancelPremium.select_user))
async def cancel_premium_process(
    message: Message, l10n: FluentLocalization, state: FSMContext
):
    """
    Selects the user to cancel the Books_Base Premium status.
    :param message: A message with the expected username or user ID.
    :param l10n: Language set by the user.
    :param state: FSM (CancelPremium).
    :return: Cancel the Books_Base Premium status of a user.
    """

    user, response_message = await find_user(message.text, l10n)

    if user:
        id_user = user["id_user"]
        fullname = user["fullname"]
        username = user["username"]
        url_user = await create_user_link(fullname, username)

        response = await api.premium.delete_premium(id_user)
        status = response.status

        if status == 204:
            await message.answer(
                l10n.format_value(
                    "cancel-premium-success",
                    {"url_user": url_user, "id_user": str(id_user)},
                )
            )
            await state.clear()
        else:
            sent_message = await message.answer(
                l10n.format_value(
                    "cancel-premium-error",
                    {"url_user": url_user, "id_user": str(id_user)},
                ),
                reply_markup=cancel_keyboard(l10n),
            )
            await state.update_data(sent_message_id=sent_message.message_id)
    else:
        sent_message = await message.answer(
            response_message, reply_markup=cancel_keyboard(l10n)
        )
        await state.update_data(sent_message_id=sent_message.message_id)
