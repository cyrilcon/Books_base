from aiogram import Router, F, Bot
from aiogram.exceptions import AiogramError
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from api.books_base_api.schemas import PaymentCurrencyEnum, PaymentTypeEnum
from tg_bot.config import config
from tg_bot.enums import MessageEffects
from tg_bot.keyboards.inline import cancel_keyboard, my_books_keyboard
from tg_bot.services import (
    ClearKeyboard,
    generate_book_caption,
    is_valid_book_article,
    get_user_localization,
    Payment,
    get_fluent_localization,
)
from tg_bot.states import GiveBook

give_book_step_2_router = Router()


@give_book_step_2_router.callback_query(
    StateFilter(GiveBook.select_book),
    F.data == "back",
)
async def back_to_give_book_step_1(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_text(
        l10n.format_value("give-book-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(GiveBook.select_user)
    await call.answer()


@give_book_step_2_router.message(
    StateFilter(GiveBook.select_book),
    F.text,
)
async def give_book_step_2(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    await ClearKeyboard.clear(message, storage)

    article = message.text

    if not is_valid_book_article(article):
        sent_message = await message.answer(
            l10n.format_value("give-book-error-invalid-article"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    id_book = int(article.lstrip("#"))

    response = await api.books.get_book_by_id(id_book=id_book)
    status = response.status

    if status != 200:
        sent_message = await message.answer(
            l10n.format_value("give-book-error-article-not-found"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    book = response.get_model()

    data = await state.get_data()
    id_user_recipient = data.get("id_user_recipient")
    user_link = data.get("user_link")

    response = await api.users.get_book_ids(id_user=id_user_recipient)
    book_ids = response.result

    if id_book in book_ids:
        sent_message = await message.answer(
            l10n.format_value(
                "give-book-error-user-already-has-this-book",
                {"title": book.title, "article": article},
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    l10n_recipient = await get_user_localization(id_user_recipient)
    caption = await generate_book_caption(
        book_data=book,
        l10n=l10n_recipient,
        id_user=id_user_recipient,
    )

    try:
        await bot.send_message(
            chat_id=id_user_recipient,
            text=l10n.format_value(
                "give-book-success-message-for-user",
                {"title": book.title},
            ),
            message_effect_id=MessageEffects.CONFETTI,
        )
        await bot.send_photo(
            chat_id=id_user_recipient,
            photo=book.cover,
            caption=caption,
            reply_markup=my_books_keyboard(
                l10n=l10n,
                book_ids=[id_book],
            ),
        )
    except AiogramError:
        await message.answer(l10n.format_value("error-user-blocked-bot"))
    else:
        payment = Payment(amount=0)
        payment.create()
        await api.payments.create_payment(
            id_payment=payment.id,
            id_user=id_user_recipient,
            price=0,
            currency=PaymentCurrencyEnum.RUB,
            type=PaymentTypeEnum.BOOK,
            book_ids=[id_book],
        )

        l10n_params = {
            "msg_id": "give-book-success",
            "args": {
                "user_link": user_link,
                "id_user": str(id_user_recipient),
                "title": book.title,
                "article": article,
            },
        }

        await message.answer(
            l10n.format_value(l10n_params["msg_id"], l10n_params["args"])
        )

        l10n_chat = get_fluent_localization(config.chat.language_code)
        await bot.send_message(
            chat_id=config.chat.payment,
            text=l10n_chat.format_value(l10n_params["msg_id"], l10n_params["args"]),
        )
    await state.clear()
