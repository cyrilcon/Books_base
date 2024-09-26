from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.keyboards.inline import (
    cancel_keyboard,
    edit_book_keyboard,
    done_clear_cancel_keyboard,
)
from tg_bot.services import BookFormatter
from tg_bot.services import ClearKeyboard, generate_book_caption, send_files
from tg_bot.states import EditBook

edit_files_router = Router()


@edit_files_router.callback_query(F.data.startswith("edit_files"))
async def edit_files(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    await ClearKeyboard.clear(call, storage)

    id_book = int(call.data.split(":")[-1])
    response = await api.books.get_book_by_id(id_book)
    book = response.get_model()

    await send_files(
        bot=bot,
        chat_id=call.from_user.id,
        caption=book.title,
        files=book.files,
    )

    sent_message = await call.message.answer(
        l10n.format_value("edit-book-prompt-files"),
        reply_markup=cancel_keyboard(l10n),
    )

    await state.update_data(id_book_edited=id_book)
    await state.set_state(EditBook.edit_files)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=call.from_user.id,
        sent_message_id=sent_message.message_id,
    )
    await call.answer()


@edit_files_router.message(StateFilter(EditBook.edit_files), F.document)
async def edit_files_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    data = await state.get_data()
    files = data.get("files")

    file_token = message.document.file_id
    file_format = message.document.file_name.split(".")[-1]

    if files is None:
        files = []

    if any(file["format"] == file_format for file in files):
        text = "edit-book-error-file-already-sent"
    else:
        file_dict = {"format": file_format, "file_token": file_token}
        files.append(file_dict)
        text = "edit-book-prompt-more-files"

    formats = BookFormatter.format_file_formats(files)
    text = l10n.format_value(text, {"formats": formats})

    await state.update_data(files=files)
    sent_message = await message.answer(
        text,  # TODO: add delete button (future feature)
        reply_markup=done_clear_cancel_keyboard(l10n),
    )
    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@edit_files_router.callback_query(StateFilter(EditBook.edit_files), F.data == "done")
async def edit_files_done(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    data = await state.get_data()
    id_book_edited = data.get("id_book_edited")
    files = data.get("files")

    response = await api.books.get_book_by_id(id_book_edited)
    book = response.get_model()

    caption = await generate_book_caption(book_data=book, l10n=l10n)
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

    response = await api.books.update_book(id_book_edited, files=files)
    book = response.get_model()

    caption = await generate_book_caption(book_data=book, l10n=l10n)

    await call.message.edit_text(l10n.format_value("edit-book-success"))

    await send_files(
        bot=bot,
        chat_id=call.from_user.id,
        caption=book.title,
        files=book.files,
    )

    await call.message.answer_photo(
        photo=book.cover,
        caption=caption,
        reply_markup=edit_book_keyboard(l10n, book.id_book),
    )
    await state.clear()
    await call.answer()


@edit_files_router.callback_query(StateFilter(EditBook.edit_files), F.data == "clear")
async def edit_files_clear(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_text(
        l10n.format_value("edit-book-prompt-files"),
        reply_markup=cancel_keyboard(l10n),
    )
    files = []
    await state.update_data(files=files)
    await call.answer()
