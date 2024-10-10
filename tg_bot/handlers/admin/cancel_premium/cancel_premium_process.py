from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.services import find_user, create_user_link
from tg_bot.states import CancelPremium

cancel_premium_process_router = Router()


@cancel_premium_process_router.message(
    StateFilter(CancelPremium.select_user),
    F.text,
)
async def cancel_premium_process(
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

    if not user.is_premium:
        await message.answer(
            l10n.format_value(
                "cancel-premium-error-user-already-has-not-premium",
                {"user_link": user_link, "id_user": str(id_user)},
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    await api.users.premium.delete_premium(id_user=id_user)
    await message.answer(
        l10n.format_value(
            "cancel-premium-success",
            {"user_link": user_link, "id_user": str(id_user)},
        )
    )
    await state.clear()
