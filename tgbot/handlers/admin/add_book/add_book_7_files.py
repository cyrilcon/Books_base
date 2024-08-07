from typing import Dict, List, Tuple

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import (
    back_cancel_keyboard,
    done_clear_back_cancel_keyboard,
    price_post_keyboard,
)
from tgbot.services import ClearKeyboard
from tgbot.states import AddBook

add_book_router_7 = Router()
add_book_router_7.message.filter(AdminFilter())


@add_book_router_7.callback_query(StateFilter(AddBook.add_files), F.data == "back")
async def back_to_add_book_6(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("add-book-cover"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.set_state(AddBook.add_cover)


@add_book_router_7.message(StateFilter(AddBook.add_files), F.document)
async def add_book_7(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    data = await state.get_data()
    files = data.get("files")
    files, text = await add_formats_to_dict(message, l10n, files)

    await state.update_data(files=files)
    sent_message = await message.answer(
        text, reply_markup=done_clear_back_cancel_keyboard(l10n)
    )
    await ClearKeyboard.safe_message(
        storage=storage,
        user_id=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@add_book_router_7.callback_query(StateFilter(AddBook.add_files), F.data == "done")
async def done_add_book_7(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("add-book-price"),
        reply_markup=price_post_keyboard(l10n),
    )
    await state.set_state(AddBook.select_price)


@add_book_router_7.callback_query(StateFilter(AddBook.add_files), F.data == "clear")
async def clear_add_book_7(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("add-book-files"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    files = []
    await state.update_data(files=files)


async def add_formats_to_dict(
    message: Message,
    l10n: FluentLocalization,
    files: List[Dict[str, str]],
) -> Tuple[List[Dict[str, str]], str]:
    """
    Adds files and their formats to the dictionary.
    :param message: Expected book file.
    :param l10n: Language set by the user.
    :param files: Files of the book.
    :return: Dictionary with files and their formats.
    """

    file = message.document.file_id
    file_format = message.document.file_name.split(".")[-1]

    if files is None:
        files = []

    if any(file["format"] == file_format for file in files):
        selected_text = "add-book-files-already-sent"
    else:
        file_dict = {"format": file_format, "file": file}
        files.append(file_dict)
        selected_text = "add-book-files-send-more"

    formats = ", ".join(f"{file['format']}" for file in files)
    text = l10n.format_value(selected_text, {"formats": formats})

    return files, text
