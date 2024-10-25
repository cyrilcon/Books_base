from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from config import config
from tg_bot.api_client import api
from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.services import find_user, create_user_link, get_fluent_localization
from tg_bot.states import TakeDiscount

take_discount_process_router = Router()


@take_discount_process_router.message(
    StateFilter(TakeDiscount.select_user),
    F.text,
)
async def take_discount_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    bot: Bot,
):
    user, response_message = await find_user(l10n, message.text)

    if not user:
        await message.answer(response_message, reply_markup=cancel_keyboard(l10n))
        return

    id_user = user.id_user
    user_link = create_user_link(user.full_name, user.username)

    if not user.has_discount:
        await message.answer(
            l10n.format_value(
                "take-discount-error-user-already-has-not-discount",
                {"user_link": user_link, "id_user": str(id_user)},
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    await api.users.discounts.delete_discount(id_user=id_user)

    l10n_params = {
        "msg_id": "take-discount-success",
        "args": {
            "discount": user.has_discount,
            "user_link": user_link,
            "id_user": str(id_user),
        },
    }

    await message.answer(
        l10n.format_value(
            msg_id=l10n_params["msg_id"],
            args=l10n_params["args"],
        )
    )

    l10n_chat = get_fluent_localization(config.chat.language_code)
    await bot.send_message(
        chat_id=config.chat.payment,
        text=l10n_chat.format_value(
            msg_id=l10n_params["msg_id"],
            args=l10n_params["args"],
        ),
    )
    await state.clear()
