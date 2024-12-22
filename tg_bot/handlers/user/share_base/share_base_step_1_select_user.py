from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, LinkPreviewOptions
from aiogram.utils.deep_linking import create_start_link
from fluent.runtime import FluentLocalization

from config import config
from tg_bot.api_client import api
from tg_bot.keyboards.inline import (
    cancel_keyboard,
    copy_invite_link_cancel_keyboard,
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
    bot: Bot,
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

    if response.status != 200:
        invite_link = await create_start_link(bot, str(message.from_user.id))
        price_discount_100 = config.price.discount.discount_100

        await message.answer(
            l10n.format_value(
                "share-base-error-user-not-found",
                {
                    "username": username,
                    "invite_link": invite_link,
                    "price_discount_100": price_discount_100,
                },
            ),
            link_preview_options=LinkPreviewOptions(prefer_small_media=True),
            reply_markup=copy_invite_link_cancel_keyboard(
                l10n, invite_link=invite_link
            ),
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
