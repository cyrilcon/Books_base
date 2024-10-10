import random

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery, Message
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from api.books_base_api.schemas import PaymentCurrencyEnum, PaymentTypeEnum, UserSchema
from tg_bot.config import config
from tg_bot.enums import MessageEffects
from tg_bot.keyboards.inline import channel_keyboard
from tg_bot.services import (
    ClearKeyboard,
    Payment,
    create_user_link,
    BookFormatter,
    send_files,
    get_fluent_localization,
)
from tg_bot.states import Payment as PaymentState
from .keyboards import pay_set_keyboard

payment_set_router = Router()


# TODO: ДОБАВИТЬ МИДЛВАРЬ С СУББОТОЙ
@payment_set_router.callback_query(F.data.startswith("buy_set"))
async def buy_set(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    user: UserSchema,
    bot: Bot,
):
    await ClearKeyboard.clear(call, storage)
    await state.clear()

    book_ids = list(map(int, call.data.split(":")[-1].split(",")))

    response = await api.users.get_book_ids(id_user=user.id_user)
    user_book_ids = response.result

    for id_book in book_ids:
        response = await api.books.get_book_by_id(id_book=id_book)
        status = response.status

        if status != 200:
            await call.message.edit_reply_markup()
            article = BookFormatter.format_article(id_book=id_book)

            await call.message.answer(
                l10n.format_value(
                    "payment-set-error-book-unavailable",
                    {"article": article},
                )
            )
            await call.answer()
            return

        if id_book in user_book_ids:
            await call.message.edit_reply_markup()

            book = response.get_model()

            await call.message.answer(
                l10n.format_value(
                    "payment-set-error-user-already-has-this-book",
                    {"title": book.title},
                )
            )
            await call.answer()
            return

    price_rub = config.price.set.rub
    price_xtr = config.price.set.xtr

    payment = Payment(
        amount=price_rub,
        comment=l10n.format_value("saturday-action"),
    )
    payment.create()
    id_payment = payment.id

    sent_message = await call.message.answer_invoice(
        title=l10n.format_value("saturday-action"),
        description=l10n.format_value(
            "payment-set",
            {"price_rub": price_rub, "price_xtr": price_xtr},
        ),
        prices=[LabeledPrice(label="XTR", amount=price_xtr)],
        provider_token="",
        payload="set",
        currency="XTR",
        reply_markup=pay_set_keyboard(
            l10n=l10n,
            book_ids=book_ids,
            url_payment=payment.invoice,
            price_rub=price_rub,
            price_xtr=price_xtr,
            id_payment=id_payment,
        ),
    )
    await state.set_state(PaymentState.set)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=call.from_user.id,
        sent_message_id=sent_message.message_id,
    )
    await call.answer()


@payment_set_router.callback_query(
    StateFilter(PaymentState.book),
    F.data.startswith("paid_set"),
)
async def payment_set(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    user: UserSchema,
    bot: Bot,
):
    id_payment = call.data.split(":")[-2]
    book_ids = list(map(int, call.data.split(":")[-1].split(",")))

    response = await api.users.get_book_ids(id_user=user.id_user)
    user_book_ids = response.result

    for id_book in book_ids:
        response = await api.books.get_book_by_id(id_book=id_book)
        status = response.status

        if status != 200:
            await call.message.edit_reply_markup()
            article = BookFormatter.format_article(id_book=id_book)

            await call.message.answer(
                l10n.format_value(
                    "payment-set-error-book-unavailable",
                    {"article": article},
                )
            )
            await call.answer()
            return

        if id_book in user_book_ids:
            await call.message.edit_reply_markup()

            book = response.get_model()

            await call.message.answer(
                l10n.format_value(
                    "payment-set-error-user-already-has-this-book",
                    {"title": book.title},
                )
            )
            await call.answer()
            return

    price = config.price.saturday.rub

    if not Payment.check_payment(Payment(amount=price, id=id_payment)):
        await call.message.answer(l10n.format_value("payment-error-payment-not-found"))
        await call.answer()
        return

    await call.message.edit_reply_markup()

    await api.payments.create_payment(
        id_payment=id_payment,
        id_user=user.id_user,
        price=price,
        currency=PaymentCurrencyEnum.RUB,
        type=PaymentTypeEnum.BOOK,
        book_ids=book_ids,
    )

    response = await api.books.get_book_by_id(id_book=id_book)
    book = response.get_model()

    await call.message.answer(
        l10n.format_value(
            "payment-check",
            {"id_payment": id_payment},
        ),
    )

    await send_files(
        bot=bot,
        chat_id=user.id_user,
        caption=book.title,
        files=book.files,
    )

    base = random.randint(7, 15) if price == 50 else random.randint(10, 20)
    await api.users.update_user(
        id_user=user.id_user,
        base_balance=user.base_balance + base,
    )

    if user.has_discount:
        await api.users.discounts.delete_discount(id_user=user.id_user)

    await call.message.answer(
        l10n.format_value(
            "payment-book-success",
            {
                "base": base,
                "channel_link": config.channel.link,
            },
        ),
        message_effect_id=MessageEffects.CONFETTI,
        reply_markup=channel_keyboard(l10n),
    )
    await state.clear()

    user_link = create_user_link(user.full_name, user.username)

    l10n_chat = get_fluent_localization(config.chat.language_code)
    await bot.send_message(
        chat_id=config.chat.payment,
        text=l10n_chat.format_value(
            "payment-book-paid-message-for-admin",
            {
                "user_link": user_link,
                "id_user": str(user.id_user),
                "title": book.title,
                "article": BookFormatter.format_article(book.id_book),
                "price": price,
                "currency": "₽",
                "base": base,
                "id_payment": id_payment,
            },
        ),
    )
    await call.answer()
