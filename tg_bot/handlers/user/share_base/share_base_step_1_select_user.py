from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.api_client import api
from tg_bot.keyboards.inline import (
    cancel_keyboard,
    share_our_store_keyboard,
    share_base_keyboard,
)
from tg_bot.services import extract_username
from tg_bot.states import ShareBase

share_base_step_1_router = Router()


@share_base_step_1_router.message(
    StateFilter(ShareBase.select_user),
    F.text,
)
async def share_base_step_1(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    id_user = message.from_user.id

    username = extract_username(message.text)

    if not username:
        await message.answer(
            l10n.format_value("share-base-error-invalid-username"),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    if username == message.from_user.username:
        await message.answer(
            l10n.format_value("share-base-error-self-transfer"),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    response = await api.users.get_user_by_username(username=username)
    status = response.status

    if status != 200:
        await message.answer(
            l10n.format_value(
                "share-base-error-user-not-found",
                {"username": username},
            ),
            reply_markup=share_our_store_keyboard(l10n),
        )
        return

    user = response.get_model()

    if user.is_premium:
        await message.answer(
            l10n.format_value(
                "share-base-error-user-has-premium",
                {"username": username},
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    response = await api.users.get_user_by_id(id_user=id_user)
    base_balance = response.get_model().base_balance

    await message.answer(
        l10n.format_value(
            "share-base-transfer",
            {"username": username, "base_balance": base_balance},
        ),
        reply_markup=share_base_keyboard(l10n, base=base_balance),
    )
    await state.set_state(ShareBase.transfer)
