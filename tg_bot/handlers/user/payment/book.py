from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery, LabeledPrice
from fluent.runtime import FluentLocalization

from tg_bot.api.books_base_api import api
from tg_bot.config import config
from tg_bot.keyboards.inline import pay_book_keyboard
from tg_bot.services import ClearKeyboard
from tg_bot.services import Payment
from tg_bot.states import Payment as PaymentState

payment_book_router = Router()


@payment_book_router.callback_query(F.data.startswith("buy_book"))
async def payment_book(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    price = int(call.data.split(":")[-2])
    id_book = call.data.split(":")[-1]

    response = await api.books.get_book_by_id(id_book)
    status = response.status

    if status != 200:
        await call.message.answer(l10n.format_value("buy-book-error-book-unavailable"))
        return

    book = response.get_model()

    price_rub = config.price.book.basic.rub
    price_stars = config.price.book.basic.xtr

    if price == 85:
        # TODO: проверить скидку у пользователя и от этого выдавать цену
        pass

    payment = Payment(
        amount=price_rub,
        comment=book.title,
    )
    payment.create()

    sent_message = await call.message.answer_invoice(
        title=book.title,
        description=l10n.format_value(
            "buy-book",
            {"price_rub": price_rub, "price_stars": price_stars},
        ),
        prices=[LabeledPrice(label="XTR", amount=price_stars)],
        provider_token="",
        payload=f"payment_book:{id_book}",
        currency="XTR",
        reply_markup=pay_book_keyboard(
            l10n=l10n,
            url_payment=payment.invoice,
            price_stars=price_stars,
            price_rub=price_rub,
            id_payment=payment.id,
        ),
    )
    await state.set_state(PaymentState.book)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=call.from_user.id,
        sent_message_id=sent_message.message_id,
    )
