from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tgbot.keyboards.inline import cancel_keyboard
from tgbot.services import (
    find_user,
    create_user_link,
    ClearKeyboard,
    convert_utc_datetime,
)
from tgbot.states import GetProfile

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
        l10n.format_value("get-profile-prompt-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(GetProfile.select_user)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@get_profile_router.message(StateFilter(GetProfile.select_user), F.text)
async def get_profile_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    user, response_message = await find_user(message.text, l10n)

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

    user_link = await create_user_link(user.full_name, user.username)

    registration_datetime = convert_utc_datetime(user.registration_datetime)
    last_activity_datetime = convert_utc_datetime(user.last_activity_datetime)

    country_flag = get_country_flag(user.language_code)
    status_icons = get_user_status_icons(user, l10n)

    discount = user.has_discount
    if discount == 100:
        discount_message = (
            "\n" + l10n.format_value("get-profile-user-has-free-book") + "\n"
        )
    elif discount > 0:
        discount_message = (
            "\n"
            + l10n.format_value("get-profile-user-has-discount", {"discount": discount})
            + "\n"
        )
    else:
        discount_message = ""

    await message.answer(
        l10n.format_value(
            "get-profile-template",
            {
                "status_icons": status_icons,
                "user_link": user_link,
                "id_user": str(user.id_user),
                "country_flag": country_flag,
                "discount": discount_message,
                "base_balance": user.base_balance,
                "registration_datetime": registration_datetime,
                "last_activity_datetime": last_activity_datetime,
            },
        )
    )
    await state.clear()


def get_country_flag(language_code):
    flags = {
        "uk": "🇺🇦",
        "ru": "🇷🇺",
        "en": "🇬🇧",
    }
    return flags.get(language_code, "🏳️")


def get_user_status_icons(user, l10n):
    icons = []
    if user.is_admin:
        icons.append(l10n.format_value("get-profile-status-icon-admin"))
    if user.is_blacklisted:
        icons.append(l10n.format_value("get-profile-status-icon-blacklisted"))
    if user.is_premium:
        icons.append(l10n.format_value("get-profile-status-icon-premium"))
    return "".join(icons)
