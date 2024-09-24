from aiogram import Router, F, Bot
from aiogram.exceptions import AiogramError
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.api.books_base_api import api
from tg_bot.config import config
from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.schemas import PaymentCurrencyEnum
from tg_bot.services import ClearKeyboard, create_user_link
from tg_bot.states import Refund

refund_router = Router()


@refund_router.message(Command("refund"))
async def refund(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("refund"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(Refund.select_payment)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@refund_router.message(StateFilter(Refund.select_payment), F.text)
async def refund_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    await ClearKeyboard.clear(message, storage)

    id_payment = message.text

    response = await api.payments.get_payment_by_id(id_payment=id_payment)
    status = response.status

    if status != 200:
        sent_message = await message.answer(
            l10n.format_value("refund-error-not-found"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    payment = response.get_model()

    if payment.currency != PaymentCurrencyEnum.XTR:
        sent_message = await message.answer(
            l10n.format_value("refund-error-currency-unavailable"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
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
        response = await api.users.get_user_by_id(id_user)
        user = response.get_model()

        full_name = user.full_name
        username = user.username
        user_link = await create_user_link(full_name, username)

        text = l10n.format_value(
            "refund-success",
            {
                "user_link": user_link,
                "id_user": str(id_user),
                "stars": payment.price,
            },
        )
        await message.answer(text=text)
        await bot.send_message(chat_id=config.chat.payment, text=text)
    await state.clear()
