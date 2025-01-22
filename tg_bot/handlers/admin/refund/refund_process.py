from aiogram import Router, F, Bot
from aiogram.exceptions import AiogramError
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from api.api_v1.schemas import PaymentCurrencyEnum
from config import config
from tg_bot.api_client import api
from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.services.localization import get_fluent_localization
from tg_bot.services.users import create_user_link
from tg_bot.states import Refund

refund_process_router = Router()


@refund_process_router.message(
    StateFilter(Refund.select_payment),
    F.text,
)
async def refund_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    bot: Bot,
):
    id_payment = message.text

    response = await api.payments.get_payment_by_id(id_payment=id_payment)

    if response.status != 200:
        await message.answer(
            l10n.format_value("refund-error-not-found"),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    payment = response.get_model()

    if payment.currency != PaymentCurrencyEnum.XTR:
        await message.answer(
            l10n.format_value("refund-error-currency-unavailable"),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    id_user = payment.id_user

    try:
        await bot.refund_star_payment(
            user_id=id_user,
            telegram_payment_charge_id=id_payment,
        )
    except AiogramError:
        await message.answer(l10n.format_value("error-user-blocked-bot"))
    else:
        response = await api.users.get_user_by_id(id_user=id_user)
        user = response.get_model()

        user_link = create_user_link(user.full_name, user.username)

        l10n_params = {
            "msg_id": "refund-success",
            "args": {
                "user_link": user_link,
                "id_user": str(id_user),
                "stars": payment.price,
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
