from aiogram import Router, F, Bot
from aiogram.exceptions import AiogramError
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.enums import MessageEffects
from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.services import (
    find_user,
    create_user_link,
    set_user_commands,
    get_fluent_localization,
)
from tg_bot.states import AddAdmin

add_admin_process_router = Router()


@add_admin_process_router.message(
    StateFilter(AddAdmin.select_user),
    F.text,
)
async def add_admin_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    bot: Bot,
):
    user, response_message = await find_user(l10n, message.text)

    if not user:
        await message.answer(response_message, reply_markup=cancel_keyboard(l10n))
        return

    id_user = user.id_user
    user_link = create_user_link(user.full_name, user.username)

    if user.is_admin:
        await message.answer(
            l10n.format_value(
                "add-admin-error-user-already-admin",
                {"user_link": user_link, "id_user": str(id_user)},
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    l10n_recipient = get_fluent_localization(user.language_code)
    try:
        await bot.send_message(
            chat_id=id_user,
            text=l10n_recipient.format_value("add-admin-success-message-for-user"),
            message_effect_id=MessageEffects.CONFETTI,
        )
    except AiogramError:
        await message.answer(l10n.format_value("error-user-blocked-bot"))
    else:
        await api.users.admins.create_admin(id_user=id_user)
        await set_user_commands(bot=bot, id_user=id_user, is_admin=True)
        await message.answer(
            l10n.format_value(
                "add-admin-success",
                {"user_link": user_link, "id_user": str(id_user)},
            )
        )
    await state.clear()
