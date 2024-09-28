from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.services import ClearKeyboard, generate_book_caption, BookFormatter
from tg_bot.states import EditBook
from .keyboards import edit_book_keyboard, yes_cancel_keyboard

edit_title_router = Router()


@edit_title_router.callback_query(F.data.startswith("edit_title"))
async def edit_title(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(call, storage)

    id_book = int(call.data.split(":")[-1])
    response = await api.books.get_book_by_id(id_book=id_book)
    book = response.get_model()

    sent_message = await call.message.answer(
        l10n.format_value(
            "edit-book-title",
            {"title": book.title},
        ),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.update_data(id_book_edited=id_book)
    await state.set_state(EditBook.edit_title)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=call.from_user.id,
        sent_message_id=sent_message.message_id,
    )
    await call.answer()


@edit_title_router.message(
    StateFilter(EditBook.edit_title),
    F.text,
)
async def edit_title_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    title = message.text

    if len(title) > 255:
        sent_message = await message.answer(
            l10n.format_value("edit-book-error-title-too-long"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    if '"' in title:
        sent_message = await message.answer(
            l10n.format_value("edit-book-error-invalid-title"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    await state.update_data(title=title)

    response = await api.books.search_books_by_title(
        title=title,
        similarity_threshold=100,
    )
    result = response.get_model()

    if result.found > 0:
        book = result.books[0].book
        article = BookFormatter.format_article(book.id_book)

        sent_message = await message.answer(
            l10n.format_value(
                "edit-book-error-title-already-exists",
                {
                    "title": book.title,
                    "article": article,
                },
            ),
            reply_markup=yes_cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    data = await state.get_data()
    id_book_edited = data.get("id_book_edited")

    response = await api.books.get_book_by_id(id_book=id_book_edited)
    book = response.get_model()

    caption = await generate_book_caption(book_data=book, l10n=l10n, title=title)
    caption_length = len(caption)

    if caption_length > 1024:
        sent_message = await message.answer(
            l10n.format_value(
                "edit-book-error-caption-too-long",
                {"caption_length": caption_length},
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    await api.books.update_book(id_book_edited=id_book_edited, title=title)

    await message.answer(l10n.format_value("edit-book-success"))
    await message.answer_photo(
        photo=book.cover,
        caption=caption,
        reply_markup=edit_book_keyboard(l10n, book.id_book),
    )
    await state.clear()


@edit_title_router.callback_query(
    StateFilter(EditBook.edit_title),
    F.data == "yes",
)
async def edit_title_yes(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await call.message.edit_reply_markup()

    data = await state.get_data()
    id_book_edited = data.get("id_book_edited")
    title = data.get("title")

    response = await api.books.get_book_by_id(id_book_edited)
    book = response.get_model()

    caption = await generate_book_caption(book_data=book, l10n=l10n, title=title)
    caption_length = len(caption)

    if caption_length > 1024:
        sent_message = await call.message.answer(
            l10n.format_value(
                "edit-book-error-caption-too-long",
                {"caption_length": caption_length},
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=call.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    await api.books.update_book(id_book_edited=id_book_edited, title=title)

    await call.message.edit_text(l10n.format_value("edit-book-success"))
    await call.message.answer_photo(
        photo=book.cover,
        caption=caption,
        reply_markup=edit_book_keyboard(l10n, book.id_book),
    )
    await state.clear()
    await call.answer()
