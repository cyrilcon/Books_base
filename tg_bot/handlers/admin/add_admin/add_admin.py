from aiogram import Router, F, Bot
from aiogram.exceptions import AiogramError
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.enums import MessageEffects
from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.services import (
    find_user,
    create_user_link,
    ClearKeyboard,
    set_user_commands,
    get_fluent_localization,
)
from tg_bot.states import AddAdmin

add_admin_router = Router()


@add_admin_router.message(Command("add_admin"))
async def add_admin(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("add-admin-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(AddAdmin.select_user)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@add_admin_router.message(
    StateFilter(AddAdmin.select_user),
    F.text,
)
async def add_admin_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    await ClearKeyboard.clear(message, storage)

    user, response_message = await find_user(l10n, message.text)

    if not user:
        sent_message = await message.answer(
            response_message, reply_markup=cancel_keyboard(l10n)
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    id_user = user.id_user
    user_link = create_user_link(user.full_name, user.username)

    if user.is_admin:
        sent_message = await message.answer(
            l10n.format_value(
                "add-admin-error-user-already-admin",
                {"user_link": user_link, "id_user": str(id_user)},
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
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
