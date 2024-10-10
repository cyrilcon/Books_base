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
from tg_bot.keyboards.inline import channel_keyboard, pay_book_keyboard
from tg_bot.services import (
    Payment,
    create_user_link,
    BookFormatter,
    send_files,
    get_fluent_localization,
    ClearKeyboard,
)
from tg_bot.states import Payment as PaymentState

payment_book_router = Router()


@payment_book_router.callback_query(
    F.data.startswith("buy_book"),
    flags={
        "clear_keyboard": False,
        "safe_message": False,
        "throttle": True,
    },
)
async def buy_book(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    user: UserSchema,
    bot: Bot,
):
    await ClearKeyboard.clear(call, storage)
    await state.clear()

    id_book = int(call.data.split(":")[-1])

    response = await api.books.get_book_by_id(id_book=id_book)
    status = response.status

    if status != 200:
        await call.message.edit_reply_markup()
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

    response = await api.users.get_book_ids(id_user=user.id_user)
    book_ids = response.result

    if id_book in book_ids:
        await call.message.edit_reply_markup()

        await send_files(
            bot=bot,
            chat_id=user.id_user,
            caption=book.title,
            files=book.files,
        )
        await call.answer()
        return

    price_rub = book.price.value
    price_xtr = config.price.book.main.xtr

    payment = Payment(
        amount=price_rub,
        comment=book.title,
    )
    payment.create()
    id_payment = payment.id

    if price_rub == config.price.book.main.rub:
        discount = user.has_discount

        if discount == 100:
            await call.message.edit_reply_markup()

            await api.users.discounts.delete_discount(id_user=user.id_user)
            await api.payments.create_payment(
                id_payment=id_payment,
                id_user=user.id_user,
                price=0,
                currency=PaymentCurrencyEnum.RUB,
                type=PaymentTypeEnum.BOOK,
                book_ids=[id_book],
            )
            await send_files(
                bot=bot,
                chat_id=user.id_user,
                caption=book.title,
                files=book.files,
            )

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
            prices_rub = {
                15: round(0.85 * config.price.book.main.rub),
                30: round(0.70 * config.price.book.main.rub),
                50: round(0.50 * config.price.book.main.rub),
            }
            price_rub = prices_rub.get(discount)

            prices_xtr = {
                15: round(0.85 * config.price.book.main.xtr),
                30: round(0.70 * config.price.book.main.xtr),
                50: round(0.50 * config.price.book.main.xtr),
            }
            price_xtr = prices_xtr.get(discount)

    sent_message = await call.message.answer_invoice(
        title=book.title,
        description=l10n.format_value(
            "payment-book",
            {"price_rub": price_rub, "price_xtr": price_xtr},
        ),
        prices=[LabeledPrice(label="XTR", amount=price_xtr)],
        provider_token="",
        payload=f"book:{id_book}",
        currency="XTR",
        reply_markup=pay_book_keyboard(
            l10n=l10n,
            id_book=id_book,
            url_payment=payment.invoice,
            price_xtr=price_xtr,
            price_rub=price_rub,
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
    F.data.startswith("paid_book"),
    flags={
        "clear_keyboard": False,
        "safe_message": False,
    },
)
async def payment_book(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    user: UserSchema,
    bot: Bot,
):
    id_book = int(call.data.split(":")[-3])
    price = int(call.data.split(":")[-2])
    id_payment = call.data.split(":")[-1]

    response = await api.users.get_book_ids(id_user=user.id_user)
    book_ids = response.result

    if id_book in book_ids:
        await call.message.edit_reply_markup()
        await call.answer(
            l10n.format_value("payment-book-error-user-already-has-this-book"),
            show_alert=True,
        )
        await state.clear()
        return

    if not Payment.check_payment(Payment(amount=price, id=id_payment)):
        await call.answer(
            l10n.format_value("payment-error-payment-not-found"),
            show_alert=True,
        )
        return

    await call.message.edit_reply_markup()

    await api.payments.create_payment(
        id_payment=id_payment,
        id_user=user.id_user,
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
        chat_id=user.id_user,
        caption=book.title,
        files=book.files,
    )

    if price == config.price.book.daily.rub:
        base = random.randint(7, 15)
    else:
        base = random.randint(10, 20)

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
    await call.answer()

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


@payment_book_router.pre_checkout_query(StateFilter(PaymentState.book))
async def payment_book_on_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    id_book = int(pre_checkout_query.invoice_payload.split(":")[-1])
    id_user = pre_checkout_query.from_user.id

    response = await api.users.get_user_by_id(id_user=id_user)
    user = response.get_model()

    response = await api.users.get_book_ids(id_user=id_user)
    book_ids = response.result

    if user.is_premium or id_book in book_ids:
        l10n = get_fluent_localization(user.language_code)
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
    user: UserSchema,
    bot: Bot,
):
    id_payment = message.successful_payment.telegram_payment_charge_id
    price = float(message.successful_payment.total_amount)
    id_book = int(message.successful_payment.invoice_payload.split(":")[-1])

    await api.payments.create_payment(
        id_payment=id_payment,
        id_user=user.id_user,
        price=price,
        currency=PaymentCurrencyEnum.XTR,
        type=PaymentTypeEnum.BOOK,
        book_ids=[id_book],
    )

    await message.answer(
        l10n.format_value(
            "payment-check",
            {"id_payment": id_payment},
        ),
    )

    response = await api.books.get_book_by_id(id_book=id_book)
    book = response.get_model()

    await send_files(
        bot=bot,
        chat_id=user.id_user,
        caption=book.title,
        files=book.files,
    )

    if price == config.price.book.daily.rub:
        base = random.randint(7, 15)
    else:
        base = random.randint(10, 20)

    await api.users.update_user(
        id_user=user.id_user,
        base_balance=user.base_balance + base,
    )

    if user.has_discount:
        await api.users.discounts.delete_discount(id_user=user.id_user)

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

    # TODO: удалить на продакшене
    await bot.refund_star_payment(
        user_id=message.from_user.id,
        telegram_payment_charge_id=id_payment,
    )

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
    flags={
        "clear_keyboard": False,
        "safe_message": False,
    },
)
async def payment_book_unprocessed_messages(
    message: Message,
    l10n: FluentLocalization,
):
    await message.answer(l10n.format_value("payment-book-unprocessed-messages"))
