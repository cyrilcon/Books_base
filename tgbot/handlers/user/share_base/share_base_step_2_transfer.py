from aiogram import Router, Bot, F
from aiogram.exceptions import AiogramError
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery, LinkPreviewOptions
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.keyboards.inline import cancel_keyboard
from tgbot.services import (
    ClearKeyboard,
    get_user_language,
    create_user_link,
    extract_username,
)
from tgbot.states import ShareBase

share_base_step_2_router = Router()


@share_base_step_2_router.callback_query(F.data == "share_base_back")
async def back_to_share_base_step_1(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    sent_message = await call.message.edit_text(
        l10n.format_value("share-base-step-1-select-user"),
        reply_markup=cancel_keyboard(l10n),
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )
    await state.set_state(ShareBase.select_user)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=call.from_user.id,
        sent_message_id=sent_message.message_id,
    )
    await call.answer()


@share_base_step_2_router.callback_query(F.data.startswith("share_base"))
async def share_base_step_2(call: CallbackQuery, l10n: FluentLocalization, bot: Bot):
    base_received = int(call.data.split(":")[-1])

    username = extract_username(call.message.text)

    response = await api.users.get_user_by_username(username)
    recipient = response.get_model()
    recipient_base_balance = recipient.base_balance + base_received

    response = await api.users.get_user_by_id(call.from_user.id)
    sender = response.get_model()
    sender_base_balance = sender.base_balance - base_received

    if sender_base_balance < 0:
        await call.answer(
            l10n.format_value(
                "share-base-error-insufficient-funds",
                {"username": username},
            ),
            show_alert=True,
        )
        return

    id_recipient = recipient.id_user
    l10n_recipient = await get_user_language(id_recipient)

    user_link = await create_user_link(sender.full_name, sender.username)

    try:
        await bot.send_message(
            chat_id=id_recipient,
            text=l10n_recipient.format_value(
                "share-base-received",
                {
                    "base_received": base_received,
                    "user_link": user_link,
                    "base_balance": recipient_base_balance,
                },
            ),
            link_preview_options=LinkPreviewOptions(is_disabled=True),
        )
    except AiogramError:
        await call.answer(
            l10n.format_value("share-base-error-general"),
            show_alert=True,
        )
    else:
        await api.users.update_user(
            id_user=sender.id_user,
            base_balance=sender_base_balance,
        )
        await api.users.update_user(
            id_user=id_recipient,
            base_balance=recipient_base_balance,
        )
        await call.message.edit_text(
            l10n.format_value(
                "share-base-success",
                {
                    "base_received": base_received,
                    "username": recipient.username,
                    "base_balance": sender_base_balance,
                },
            ),
        )
        await call.answer()
