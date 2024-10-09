from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import (
    back_cancel_keyboard,
    done_clear_back_cancel_keyboard,
    add_price_keyboard,
)
from tg_bot.services import BookFormatter
from tg_bot.states import AddBook

add_book_step_7_router = Router()


@add_book_step_7_router.callback_query(
    StateFilter(AddBook.add_files),
    F.data == "back",
)
async def back_to_add_book_step_6(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_text(
        l10n.format_value("add-book-cover"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    files = []
    await state.update_data(files=files)
    await state.set_state(AddBook.add_cover)
    await call.answer()


@add_book_step_7_router.message(
    StateFilter(AddBook.add_files),
    F.document,
)
async def add_book_step_7(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    file_token = message.document.file_id
    file_format = message.document.file_name.split(".")[-1]

    data = await state.get_data()
    files = data.get("files")

    if files is None:
        files = []

    if any(file["format"] == file_format for file in files):
        text = "add-book-error-file-already-sent"
    else:
        file_dict = {"format": file_format, "file_token": file_token}
        files.append(file_dict)
        text = "add-book-more-files"

    formats = BookFormatter.format_file_formats(files)
    text = l10n.format_value(text, {"formats": formats})

    await state.update_data(files=files)
    await message.answer(text=text, reply_markup=done_clear_back_cancel_keyboard(l10n))


@add_book_step_7_router.callback_query(
    StateFilter(AddBook.add_files),
    F.data == "done",
)
async def add_book_step_7_done(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_text(
        l10n.format_value("add-book-select-price"),
        reply_markup=add_price_keyboard(l10n),
    )
    await state.set_state(AddBook.select_price)
    await call.answer()


@add_book_step_7_router.callback_query(
    StateFilter(AddBook.add_files),
    F.data == "clear",
)
async def add_book_step_7_clear(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_text(
        l10n.format_value("add-book-files"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    files = []
    await state.update_data(files=files)
    await call.answer()
