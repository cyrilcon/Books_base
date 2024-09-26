from aiogram import Router, F, Bot
from aiogram.exceptions import AiogramError
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.enums import MessageEffects
from api.books_base_api import api
from tg_bot.config import config
from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.services import (
    find_user,
    create_user_link,
    ClearKeyboard,
    get_user_localization,
)
from tg_bot.states import GivePremium

give_premium_router = Router()


@give_premium_router.message(Command("give_premium"))
async def give_premium(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("give-premium-prompt-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(GivePremium.select_user)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@give_premium_router.message(StateFilter(GivePremium.select_user), F.text)
async def give_premium_process(
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
    full_name = user.full_name
    username = user.username
    user_link = await create_user_link(full_name, username)

    if user.is_premium:
        sent_message = await message.answer(
            l10n.format_value(
                "give-premium-error-already-given",
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

    l10n_recipient = await get_user_localization(id_user)
    try:
        await bot.send_message(
            chat_id=id_user,
            text=l10n_recipient.format_value("give-premium-given"),
            message_effect_id=MessageEffects.CONFETTI,
        )
    except AiogramError:
        await message.answer(l10n.format_value("error-user-blocked-bot"))
    else:
        await api.users.premium.create_premium(id_user)
        text = l10n.format_value(
            "give-premium-success",
            {"user_link": user_link, "id_user": str(id_user)},
        )
        await message.answer(text=text)
        await bot.send_message(chat_id=config.chat.payment, text=text)
    await state.clear()
