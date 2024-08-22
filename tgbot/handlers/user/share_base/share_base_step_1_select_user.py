from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, LinkPreviewOptions
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.keyboards.inline import (
    cancel_keyboard,
    share_base_keyboard,
    share_our_store_keyboard,
)
from tgbot.services import ClearKeyboard, extract_username
from tgbot.states import ShareBase

share_base_step_1_router = Router()


@share_base_step_1_router.message(Command("share_base"))
async def share_base(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("share-base-prompt-select-user"),
        reply_markup=cancel_keyboard(l10n),
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )
    await state.set_state(ShareBase.select_user)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@share_base_step_1_router.message(StateFilter(ShareBase.select_user), F.text)
async def share_base_step_1(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    id_user = message.from_user.id

    message_text = message.text
    username = extract_username(message_text)

    if not username:
        sent_message = await message.answer(
            l10n.format_value("share-base-error-invalid-username"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    if username == message.from_user.username:
        sent_message = await message.answer(
            l10n.format_value("share-base-error-self-transfer"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    response = await api.users.get_user_by_username(username)
    status = response.status

    if status != 200:
        sent_message = await message.answer(
            l10n.format_value(
                "share-base-error-user-not-found", {"username": username}
            ),
            reply_markup=share_our_store_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    response = await api.users.get_user_by_id(id_user)
    base_balance = response.get_model().base_balance

    await message.answer(
        l10n.format_value(
            "share-base-prompt-transfer",
            {"username": username, "base_balance": base_balance},
        ),
        reply_markup=share_base_keyboard(l10n, base=base_balance),
    )
    await state.clear()
