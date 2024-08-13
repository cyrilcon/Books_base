import re

from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery, LinkPreviewOptions
from fluent.runtime import FluentLocalization

from infrastructure.books_base_api import api
from tgbot.keyboards.inline import cancel_keyboard
from tgbot.services import ClearKeyboard, get_user_language, create_user_link, Messenger
from tgbot.states import ShareBase

share_base_router_2 = Router()


@share_base_router_2.callback_query(F.data == "share_base_back")
async def back_to_share_base_1(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await call.answer(cache_time=1)
    sent_message = await call.message.edit_text(
        l10n.format_value("share-base-select-user"),
        reply_markup=cancel_keyboard(l10n),
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )
    await state.set_state(ShareBase.select_user)

    await ClearKeyboard.safe_message(
        storage=storage,
        user_id=call.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@share_base_router_2.callback_query(F.data.startswith("share_base"))
async def share_base_2(call: CallbackQuery, l10n: FluentLocalization, bot: Bot):

    base_received = int(call.data.split(":")[-1])

    pattern = r"@([a-zA-Z](?!_)(?!.*?_{2})\w{2,30}[a-zA-Z0-9])"
    username_recipient = re.search(pattern, call.message.text).group(1)

    response = await api.users.get_user_by_username(username_recipient)
    recipient = response.result

    response = await api.users.get_user_by_id(call.from_user.id)
    sender = response.result

    sender_balance = sender["base"] - base_received
    recipient_balance = recipient["base"] + base_received

    if sender_balance >= 0:
        id_recipient = recipient["id_user"]
        l10n_recipient = await get_user_language(id_recipient)

        user_link = await create_user_link(sender["fullname"], sender["username"])

        is_sent = await Messenger.safe_send_message(
            bot=bot,
            user_id=id_recipient,
            text=l10n_recipient.format_value(
                "share-base-received",
                {
                    "base_received": base_received,
                    "user_link": user_link,
                    "user_balance": recipient_balance,
                },
            ),
            link_preview_options_is_disabled=True,
        )
        if is_sent:
            await call.answer(cache_time=1)
            await api.users.update_user(
                id_user=sender["id_user"],
                base=sender_balance,
            )
            await api.users.update_user(
                id_user=id_recipient,
                base=recipient_balance,
            )
            await call.message.edit_text(
                l10n.format_value(
                    "share-base-success",
                    {
                        "base_received": base_received,
                        "username": recipient["username"],
                        "user_balance": sender_balance,
                    },
                ),
            )
        else:
            await call.answer(
                l10n.format_value("share-base-error"),
                show_alert=True,
            )
    else:
        await call.answer(
            l10n.format_value(
                "share-base-not-enough-base",
                {"username": username_recipient},
            ),
            show_alert=True,
        )
