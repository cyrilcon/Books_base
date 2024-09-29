from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.keyboards.inline import (
    back_cancel_keyboard,
    cancel_keyboard,
    buy_or_read_keyboard,
)
from tg_bot.services import ClearKeyboard, generate_book_caption, BookFormatter
from tg_bot.states import Order
from .keyboards import show_book_order_cancel_keyboard

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
        l10n.format_value("order-prompt-book-title"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(Order.book_title)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@order_step_1_router.message(
    StateFilter(Order.book_title),
    F.text,
)
async def order_step_1(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    book_title = message.text

    if len(book_title) > 255:
        sent_message = await message.answer(
            l10n.format_value("order-error-book-title-too-long"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    response = await api.books.search_books_by_title(
        title=book_title,
        similarity_threshold=100,
    )
    result = response.get_model()
    found = result.found

    if found > 0:
        book = result.books[0].book

        id_book = book.id_book
        book_title = book.title
        authors = BookFormatter.format_authors(book.authors)
        article = BookFormatter.format_article(id_book)

        sent_message = await message.answer(
            l10n.format_value(
                "order-book-error-book-already-exists",
                {"title": book_title, "authors": authors, "article": article},
            ),
            reply_markup=show_book_order_cancel_keyboard(l10n, id_book),
        )
    else:
        sent_message = await message.answer(
            l10n.format_value("order-prompt-author-name"),
            reply_markup=back_cancel_keyboard(l10n),
        )
        await state.set_state(Order.author_name)
    await state.update_data(book_title=book_title)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@order_step_1_router.callback_query(
    StateFilter(Order.book_title),
    F.data == "order",
)
async def order_step_1_confirm_order(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_text(
        l10n.format_value("order-prompt-author-name"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.set_state(Order.author_name)
    await call.answer()


@order_step_1_router.callback_query(
    StateFilter(Order.book_title),
    F.data.startswith("show_book"),
)
async def order_step_1_display_book_details(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    id_book = int(call.data.split(":")[-1])
    article = BookFormatter.format_article(id_book)

    response = await api.books.get_book_by_id(id_book=id_book)
    status = response.status

    if status != 200:
        await call.message.answer(
            l10n.format_value(
                "order-error-book-does-not-exist",
                {"article": article},
            )
        )
        return

    await call.message.edit_reply_markup()
    await state.clear()

    book = response.get_model()
    caption = await generate_book_caption(book_data=book, l10n=l10n)

    await call.message.answer_photo(
        photo=book.cover,
        caption=caption,
        reply_markup=await buy_or_read_keyboard(
            l10n=l10n,
            id_book=id_book,
            id_user=call.from_user.id,
        ),
    )
    await call.answer()
