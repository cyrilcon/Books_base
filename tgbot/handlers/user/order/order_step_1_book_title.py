from aiogram import Router, Bot, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.keyboards.inline import (
    back_cancel_keyboard,
    cancel_keyboard,
    show_book_order_cancel_keyboard,
)
from tgbot.services import ClearKeyboard, generate_book_caption, Messenger
from tgbot.states import Order

order_step_1_router = Router()


@order_step_1_router.message(Command("order"))
async def order(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("order-step-1-book-title"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(Order.book_title)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@order_step_1_router.message(StateFilter(Order.book_title), F.text)
async def order_step_1(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    book_title = message.text

    if len(book_title) <= 255:
        response = await api.books.search_books_by_title(
            book_title, similarity_threshold=100
        )
        result = response.get_model()
        found = result.found

        if found > 0:
            book = result.books[0].book

            id_book = book.id_book
            book_title = book.book_title
            authors = ", ".join([author.author_name for author in book.authors])
            article = "#{:04d}".format(id_book)

            sent_message = await message.answer(
                l10n.format_value(
                    "order-book-title-exists",
                    {"book_title": book_title, "authors": authors, "article": article},
                ),
                reply_markup=show_book_order_cancel_keyboard(l10n, id_book),
            )
        else:
            sent_message = await message.answer(
                l10n.format_value("order-step-2-author-name"),
                reply_markup=back_cancel_keyboard(l10n),
            )
            await state.set_state(Order.author_name)
        await state.update_data(book_title=book_title)
    else:
        sent_message = await message.answer(
            l10n.format_value("order-error-book-title-too-long"),
            reply_markup=cancel_keyboard(l10n),
        )

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@order_step_1_router.callback_query(StateFilter(Order.book_title), F.data == "order")
async def order_step_1_confirm_order(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("order-author-name"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.set_state(Order.author_name)


@order_step_1_router.callback_query(
    StateFilter(Order.book_title), F.data.startswith("show_book")
)
async def order_step_1_display_book_details(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    bot: Bot,
):
    await call.answer(cache_time=1)

    id_book = int(call.data.split(":")[-1])
    response = await api.books.get_book_by_id(id_book)
    status = response.status

    if status != 200:
        await call.message.answer(
            l10n.format_value(
                "order-error-book-not-exist",
                {"article": "#{:04d}".format(int(id_book))},
            )
        )
        return

    await call.message.edit_reply_markup()
    await state.clear()

    book = response.result
    caption = await generate_book_caption(data=book, l10n=l10n)

    await Messenger.safe_send_message(
        bot=bot,
        user_id=call.from_user.id,
        text=caption,
        photo=book["cover"],
        # reply_markup=deep_link_buy_keyboard(deep_link),  # TODO: добавить кнопку "Купить"
    )
