import random

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery, Message
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from api.books_base_api.schemas import PaymentCurrencyEnum, PaymentTypeEnum
from tg_bot.config import config
from tg_bot.enums import MessageEffects
from tg_bot.keyboards.inline import channel_keyboard
from tg_bot.services import (
    ClearKeyboard,
    Payment,
    create_user_link,
    BookFormatter,
    get_user_localization,
    send_files,
    get_fluent_localization,
)
from tg_bot.states import Payment as PaymentState
from .keyboards import pay_book_keyboard

payment_book_router = Router()


@payment_book_router.callback_query(F.data.startswith("buy_book"))
async def buy_book(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    await ClearKeyboard.clear(call, storage)
    await state.clear()

    price = int(call.data.split(":")[-2])
    id_book = int(call.data.split(":")[-1])

    id_user = call.from_user.id

    response = await api.books.get_book_by_id(id_book=id_book)
    status = response.status

    if status != 200:
        article = BookFormatter.format_article(id_book=id_book)

        await call.message.answer(
            l10n.format_value(
                "error-book-unavailable",
                {"article": article},
            )
        )
        await call.answer()
        return

    book = response.get_model()

    response = await api.users.get_book_ids(id_user)
    book_ids = response.result

    if id_book in book_ids:
        await call.message.edit_reply_markup()

        await send_files(
            bot=bot,
            chat_id=id_user,
            caption=book.title,
            files=book.files,
        )
        await call.answer()
        return

    payment = Payment(
        amount=price,
        comment=book.title,
    )
    payment.create()
    id_payment = payment.id

    if price == 85:
        response = await api.users.get_user_by_id(id_user=id_user)
        user = response.get_model()
        discount = user.has_discount

        if discount == 100:
            await call.message.edit_reply_markup()

            await api.users.discounts.delete_discount(id_user=id_user)
            await api.payments.create_payment(
                id_payment=id_payment,
                id_user=id_user,
                price=0,
                currency=PaymentCurrencyEnum.RUB,
                type=PaymentTypeEnum.BOOK,
                book_ids=[id_book],
            )
            await send_files(
                bot=bot,
                chat_id=id_user,
                caption=book.title,
                files=book.files,
            )

            user_link = await create_user_link(user.full_name, user.username)

            l10n_chat = get_fluent_localization(config.chat.language_code)
            await bot.send_message(
                chat_id=config.chat.payment,
                text=l10n_chat.format_value(
                    "payment-book-paid-message-for-admin",
                    {
                        "user_link": user_link,
                        "id_user": str(id_user),
                        "title": book.title,
                        "article": BookFormatter.format_article(book.id_book),
                        "price": 0,
                        "currency": "₽",
                        "base": 0,
                        "id_payment": id_payment,
                    },
                ),
            )
            await call.answer()
            return

        elif discount:
            prices = {
                15: 72,
                30: 60,
                50: 43,
            }
            price = prices.get(discount)

    sent_message = await call.message.answer_invoice(
        title=book.title,
        description=l10n.format_value(
            "payment-book",
            {"price_rub": price, "price_xtr": price},
        ),
        prices=[LabeledPrice(label="XTR", amount=price)],
        provider_token="",
        payload=f"book:{id_book}",
        currency="XTR",
        reply_markup=pay_book_keyboard(
            l10n=l10n,
            id_book=id_book,
            url_payment=payment.invoice,
            price=price,
            id_payment=id_payment,
        ),
    )
    await state.set_state(PaymentState.book)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=call.from_user.id,
        sent_message_id=sent_message.message_id,
    )
    await call.answer()


@payment_book_router.callback_query(
    StateFilter(PaymentState.book),
    F.data.startswith("paid:book"),
)
async def payment_book(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    bot: Bot,
):
    id_book = int(call.data.split(":")[-3])
    price = float(call.data.split(":")[-2])
    id_payment = call.data.split(":")[-1]

    id_user = call.from_user.id

    response = await api.users.get_book_ids(id_user)
    book_ids = response.result

    if id_book in book_ids:
        await call.message.answer(
            l10n.format_value("payment-book-error-user-already-has-this-book")
        )
        await state.clear()
        await call.answer()
        return

    if not Payment.check_payment(Payment(amount=int(price), id=id_payment)):
        await call.message.answer(l10n.format_value("payment-error-payment-not-found"))
        await call.answer()
        return

    await call.message.edit_reply_markup()

    response = await api.users.get_user_by_id(id_user)
    user = response.get_model()

    await api.payments.create_payment(
        id_payment=id_payment,
        id_user=id_user,
        price=price,
        currency=PaymentCurrencyEnum.RUB,
        type=PaymentTypeEnum.BOOK,
        book_ids=[id_book],
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
        chat_id=id_user,
        caption=book.title,
        files=book.files,
    )

    base = random.randint(7, 15) if price == 50 else random.randint(10, 20)
    await api.users.update_user(id_user=id_user, base_balance=user.base_balance + base)

    if user.has_discount:
        await api.users.discounts.delete_discount(id_user=id_user)

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

    user_link = await create_user_link(user.full_name, user.username)

    l10n_chat = get_fluent_localization(config.chat.language_code)
    await bot.send_message(
        chat_id=config.chat.payment,
        text=l10n_chat.format_value(
            "payment-book-paid-message-for-admin",
            {
                "user_link": user_link,
                "id_user": str(id_user),
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


@payment_book_router.pre_checkout_query(StateFilter(PaymentState.book))
async def payment_book_on_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    id_book = int(pre_checkout_query.invoice_payload.split(":")[-1])

    id_user = pre_checkout_query.from_user.id
    l10n = await get_user_localization(id_user)

    response = await api.users.get_user_by_id(id_user)
    user = response.get_model()

    response = await api.users.get_book_ids(id_user)
    book_ids = response.result

    if user.is_premium or id_book in book_ids:
        await pre_checkout_query.answer(
            ok=False,
            error_message=l10n.format_value("payment-pre-checkout-failed-reason"),
        )

    await pre_checkout_query.answer(ok=True)


@payment_book_router.message(
    StateFilter(PaymentState.book),
    F.successful_payment,
)
async def payment_book_on_successful(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    await ClearKeyboard.clear(message, storage)

    id_payment = message.successful_payment.telegram_payment_charge_id
    price = float(message.successful_payment.total_amount)
    id_book = int(message.successful_payment.invoice_payload.split(":")[-1])

    # TODO: удалить на продакшене
    await bot.refund_star_payment(
        user_id=message.from_user.id,
        telegram_payment_charge_id=id_payment,
    )

    id_user = message.from_user.id

    response = await api.users.get_user_by_id(id_user)
    user = response.get_model()

    await api.payments.create_payment(
        id_payment=id_payment,
        id_user=id_user,
        price=price,
        currency=PaymentCurrencyEnum.XTR,
        type=PaymentTypeEnum.BOOK,
        book_ids=[id_book],
    )

    response = await api.books.get_book_by_id(id_book=id_book)
    book = response.get_model()

    await message.answer(
        l10n.format_value(
            "payment-check",
            {"id_payment": id_payment},
        ),
    )

    await send_files(
        bot=bot,
        chat_id=id_user,
        caption=book.title,
        files=book.files,
    )

    base = random.randint(7, 15) if price == 50 else random.randint(10, 20)
    await api.users.update_user(id_user=id_user, base_balance=user.base_balance + base)

    if user.has_discount:
        await api.users.discounts.delete_discount(id_user=id_user)

    await message.answer(
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

    user_link = await create_user_link(user.full_name, user.username)

    l10n_chat = get_fluent_localization(config.chat.language_code)
    await bot.send_message(
        chat_id=config.chat.payment,
        text=l10n_chat.format_value(
            "payment-book-paid-message-for-admin",
            {
                "user_link": user_link,
                "id_user": str(id_user),
                "title": book.title,
                "article": BookFormatter.format_article(book.id_book),
                "price": price,
                "currency": " ⭐️",
                "base": base,
                "id_payment": id_payment,
            },
        ),
    )


@payment_book_router.callback_query(
    StateFilter(PaymentState.book),
    F.data == "cancel_payment",
)
async def payment_book_cancel(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    text = l10n.format_value("payment-book-canceled")

    await state.clear()
    await call.answer(text, show_alert=True)
    await call.message.edit_reply_markup()


@payment_book_router.message(
    StateFilter(PaymentState.book),
    F.text,
)
async def payment_book_unprocessed_messages(
    message: Message,
    l10n: FluentLocalization,
):
    await message.answer(l10n.format_value("payment-book-unprocessed-messages"))
