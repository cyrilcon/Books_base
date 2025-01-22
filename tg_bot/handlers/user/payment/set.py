import random

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import (
    CallbackQuery,
    LabeledPrice,
    PreCheckoutQuery,
    Message,
    LinkPreviewOptions,
)
from fluent.runtime import FluentLocalization

from config import config
from tg_bot.api_client import api
from api.api_v1.schemas import PaymentCurrencyEnum, PaymentTypeEnum, UserSchema
from tg_bot.enums import MessageEffects
from tg_bot.keyboards.inline import channel_keyboard, pay_set_keyboard
from tg_bot.middlewares import SaturdayMiddleware
from tg_bot.services import (
    ClearKeyboard,
    Payment,
    create_user_link,
    BookFormatter,
    send_files,
)
from tg_bot.services.localization import get_fluent_localization
from tg_bot.states import Payment as PaymentState

payment_set_router = Router()
payment_set_router.message.middleware(SaturdayMiddleware())
payment_set_router.callback_query.middleware(SaturdayMiddleware())


@payment_set_router.callback_query(
    F.data.startswith("buy_set"),
    flags={
        "clear_keyboard": False,
        "safe_message": False,
        "throttle": True,
    },
)
async def buy_set(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    user: UserSchema,
):
    await ClearKeyboard.clear(call, storage)
    await state.clear()

    book_ids = list(map(int, call.data.split(":")[-1].split(",")))

    response = await api.users.get_book_ids(id_user=user.id_user)
    user_book_ids = response.result

    for id_book in book_ids:
        response = await api.books.get_book_by_id(id_book=id_book)

        if response.status != 200:
            await call.message.edit_reply_markup()
            article = BookFormatter.format_article(id_book=id_book)

            await call.answer(
                l10n.format_value(
                    "payment-set-error-book-unavailable",
                    {"article": article},
                ),
                show_alert=True,
            )
            await state.clear()
            return

        if id_book in user_book_ids:
            await call.message.edit_reply_markup()
            await call.answer(
                l10n.format_value("payment-set-error-user-already-has-this-book"),
                show_alert=True,
            )
            await state.clear()
            return

    price_rub = config.price.set.rub
    price_xtr = config.price.set.xtr

    payment = Payment(
        amount=price_rub,
        comment=l10n.format_value("saturday-action"),
    )
    payment.create()
    payment_link = await payment.invoice()

    sent_message = await call.message.answer_invoice(
        title=l10n.format_value("saturday-action"),
        description=l10n.format_value(
            "payment-set",
            {"price_rub": price_rub, "price_xtr": price_xtr},
        ),
        prices=[LabeledPrice(label="XTR", amount=price_xtr)],
        provider_token="",
        payload=f"set:{','.join(map(str, book_ids))}",
        currency="XTR",
        reply_markup=pay_set_keyboard(
            l10n=l10n,
            book_ids=book_ids,
            url_payment=payment_link,
            price_rub=price_rub,
            price_xtr=price_xtr,
            id_payment=payment.id,
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
    StateFilter(PaymentState.set),
    F.data.startswith("paid_set"),
    flags={
        "clear_keyboard": False,
        "safe_message": False,
    },
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

    books = []
    for id_book in book_ids:
        response = await api.books.get_book_by_id(id_book=id_book)

        if response.status != 200:
            await call.message.edit_reply_markup()
            article = BookFormatter.format_article(id_book=id_book)

            await call.answer(
                l10n.format_value(
                    "payment-set-error-book-unavailable",
                    {"article": article},
                ),
                show_alert=True,
            )
            await state.clear()
            return

        book = response.get_model()

        if id_book in user_book_ids:
            await call.message.edit_reply_markup()
            await call.answer(
                l10n.format_value("payment-set-error-user-already-has-this-book"),
                show_alert=True,
            )
            await state.clear()
            return

        books.append(book)

    price = config.price.set.rub

    if not await Payment(amount=price, id=id_payment).check_payment():
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
        book_ids=book_ids,
    )

    await call.message.answer(
        l10n.format_value(
            "payment-check",
            {"id_payment": id_payment},
        ),
    )

    book_titles_with_articles = []
    for book in books:
        await send_files(
            bot=bot,
            chat_id=user.id_user,
            caption=book.title,
            files=book.files,
        )

        article = BookFormatter.format_article(book.id_book)
        title_with_article = f"<code>{book.title}</code> (<code>{article}</code>)"
        book_titles_with_articles.append(title_with_article)

    base = random.randint(10, 20)
    await api.users.update_user(
        id_user=user.id_user,
        base_balance=user.base_balance + base,
    )

    await call.message.answer(
        l10n.format_value(
            "payment-set-success",
            {
                "base": base,
                "channel_link": config.channel.link,
            },
        ),
        link_preview_options=LinkPreviewOptions(
            url=config.channel.link,
            prefer_small_media=True,
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
            "payment-set-paid-message-for-admin",
            {
                "user_link": user_link,
                "id_user": str(user.id_user),
                "book_titles": "\n\n".join(book_titles_with_articles),
                "price": price,
                "currency": "₽",
                "base": base,
                "id_payment": id_payment,
            },
        ),
    )


@payment_set_router.message(
    StateFilter(PaymentState.set),
    F.successful_payment,
)
async def payment_set_on_successful(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    user: UserSchema,
    bot: Bot,
):
    id_payment = message.successful_payment.telegram_payment_charge_id
    price = float(message.successful_payment.total_amount)
    book_ids = list(
        map(int, message.successful_payment.invoice_payload.split(":")[-1].split(","))
    )

    await api.payments.create_payment(
        id_payment=id_payment,
        id_user=user.id_user,
        price=price,
        currency=PaymentCurrencyEnum.XTR,
        type=PaymentTypeEnum.BOOK,
        book_ids=book_ids,
    )

    await message.answer(
        l10n.format_value(
            "payment-check",
            {"id_payment": id_payment},
        ),
    )

    book_titles_with_articles = []
    for id_book in book_ids:
        response = await api.books.get_book_by_id(id_book=id_book)
        book = response.get_model()

        await send_files(
            bot=bot,
            chat_id=user.id_user,
            caption=book.title,
            files=book.files,
        )

        article = BookFormatter.format_article(book.id_book)
        title_with_article = f"<code>{book.title}</code> (<code>{article}</code>)"
        book_titles_with_articles.append(title_with_article)

    base = random.randint(10, 20)
    await api.users.update_user(
        id_user=user.id_user,
        base_balance=user.base_balance + base,
    )

    await message.answer(
        l10n.format_value(
            "payment-set-success",
            {
                "base": base,
                "channel_link": config.channel.link,
            },
        ),
        link_preview_options=LinkPreviewOptions(
            url=config.channel.link,
            prefer_small_media=True,
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
            "payment-set-paid-message-for-admin",
            {
                "user_link": user_link,
                "id_user": str(user.id_user),
                "book_titles": "\n\n".join(book_titles_with_articles),
                "price": price,
                "currency": " ⭐️",
                "base": base,
                "id_payment": id_payment,
            },
        ),
    )


@payment_set_router.pre_checkout_query(StateFilter(PaymentState.set))
async def payment_set_on_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    response = await api.users.get_user_by_id(id_user=pre_checkout_query.from_user.id)
    user = response.get_model()

    if user.is_premium:
        l10n = get_fluent_localization(user.language_code)
        await pre_checkout_query.answer(
            ok=False,
            error_message=l10n.format_value("payment-pre-checkout-failed-reason"),
        )

    await pre_checkout_query.answer(ok=True)


@payment_set_router.callback_query(
    StateFilter(PaymentState.set),
    F.data == "cancel_payment",
)
async def payment_book_cancel(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    text = l10n.format_value("payment-set-canceled")

    await state.clear()
    await call.answer(text, show_alert=True)
    await call.message.edit_reply_markup()


@payment_set_router.message(
    StateFilter(PaymentState.set),
    flags={
        "clear_keyboard": False,
        "safe_message": False,
    },
)
async def payment_set_unprocessed_messages(
    message: Message,
    l10n: FluentLocalization,
):
    await message.answer(l10n.format_value("payment-set-unprocessed-messages"))
