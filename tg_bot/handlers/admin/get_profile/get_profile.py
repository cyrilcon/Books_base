from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.services import (
    find_user,
    create_user_link,
    ClearKeyboard,
    convert_utc_datetime,
)
from tg_bot.states import GetProfile

get_profile_router = Router()


@get_profile_router.message(Command("get_profile"))
async def get_profile(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("get-profile-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(GetProfile.select_user)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@get_profile_router.message(
    StateFilter(GetProfile.select_user),
    F.text,
)
async def get_profile_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
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

    status_icons = get_user_status_icons(user, l10n)

    user_link = create_user_link(user.full_name, user.username)

    registration_datetime = convert_utc_datetime(user.registration_datetime)
    last_activity_datetime = convert_utc_datetime(user.last_activity_datetime)

    await message.answer(
        l10n.format_value(
            "get-profile-template",
            {
                "status_icons": status_icons,
                "user_link": user_link,
                "id_user": str(user.id_user),
                "language_code": user.language_code,
                "discount": user.has_discount,
                "base_balance": user.base_balance,
                "registration_datetime": registration_datetime,
                "last_activity_datetime": last_activity_datetime,
            },
        )
    )
    await state.clear()


def get_user_status_icons(user, l10n):
    icons = []
    if user.is_admin:
        icons.append(l10n.format_value("get-profile-status-icon-admin"))
    if user.is_blacklisted:
        icons.append(l10n.format_value("get-profile-status-icon-blacklisted"))
    if user.is_premium:
        icons.append(l10n.format_value("get-profile-status-icon-premium"))
    return "".join(icons)
