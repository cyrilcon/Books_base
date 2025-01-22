from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.api_client import api
from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.services.users import create_user_link, find_user
from tg_bot.states import AddBlacklist

add_blacklist_process_router = Router()


@add_blacklist_process_router.message(
    StateFilter(AddBlacklist.select_user),
    F.text,
)
async def add_blacklist_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    user, response_message = await find_user(l10n, message.text)

    if not user:
        await message.answer(response_message, reply_markup=cancel_keyboard(l10n))
        return

    id_user = user.id_user
    user_link = create_user_link(user.full_name, user.username)

    if user.is_blacklisted:
        await message.answer(
            l10n.format_value(
                "add-blacklist-error-user-already-blacklisted",
                {"user_link": user_link, "id_user": str(id_user)},
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    await api.users.blacklist.create_blacklist(id_user=id_user)
    await message.answer(
        l10n.format_value(
            "add-blacklist-success",
            {"user_link": user_link, "id_user": str(id_user)},
        )
    )
    await state.clear()
