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
from tgbot.services import ClearKeyboard, check_username
from tgbot.states import ShareBase

share_base_router_1 = Router()


@share_base_router_1.message(Command("share_base"))
async def share_base_1(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("share-base-select-user"),
        reply_markup=cancel_keyboard(l10n),
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )
    await state.set_state(ShareBase.select_user)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@share_base_router_1.message(StateFilter(ShareBase.select_user), F.text)
async def share_base_1_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    id_user = message.from_user.id

    message_text = message.text
    selected_user = check_username(message_text)

    if selected_user:
        if selected_user == message.from_user.username:
            sent_message = await message.answer(
                l10n.format_value("share-base-error-self-send"),
                reply_markup=cancel_keyboard(l10n),
            )
            await ClearKeyboard.safe_message(
                storage=storage,
                id_user=message.from_user.id,
                sent_message_id=sent_message.message_id,
            )
        else:
            response = await api.users.get_user_by_username(selected_user)
            status = response.status

            if status == 200:
                response = await api.users.get_user_by_id(id_user)
                user_balance = response.result["base"]

                await message.answer(
                    l10n.format_value(
                        "share-base-send-base",
                        {"username": selected_user, "user_balance": user_balance},
                    ),
                    reply_markup=share_base_keyboard(l10n, base=user_balance),
                )
                await state.clear()
            else:
                sent_message = await message.answer(
                    l10n.format_value(
                        "share-base-user-not-found", {"username": selected_user}
                    ),
                    reply_markup=share_our_store_keyboard(l10n),
                )
                await ClearKeyboard.safe_message(
                    storage=storage,
                    id_user=message.from_user.id,
                    sent_message_id=sent_message.message_id,
                )
    else:
        sent_message = await message.answer(
            l10n.format_value("share-base-username-incorrect"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
