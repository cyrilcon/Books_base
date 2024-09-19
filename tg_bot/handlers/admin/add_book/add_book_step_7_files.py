from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import (
    back_cancel_keyboard,
    done_clear_back_cancel_keyboard,
    create_price_keyboard,
)
from tg_bot.services import ClearKeyboard, parse_and_format_files
from tg_bot.states import AddBook

add_book_step_7_router = Router()


@add_book_step_7_router.callback_query(StateFilter(AddBook.add_files), F.data == "back")
async def back_to_add_book_step_6(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_text(
        l10n.format_value("add-book-prompt-cover"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    files = []
    await state.update_data(files=files)
    await state.set_state(AddBook.add_cover)

    await call.answer()


@add_book_step_7_router.message(StateFilter(AddBook.add_files), F.document)
async def add_book_step_7(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    data = await state.get_data()
    files = data.get("files")
    files, text = await parse_and_format_files(message, l10n, files)

    await state.update_data(files=files)
    sent_message = await message.answer(
        text, reply_markup=done_clear_back_cancel_keyboard(l10n)
    )
    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@add_book_step_7_router.callback_query(StateFilter(AddBook.add_files), F.data == "done")
async def add_book_step_7_done(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_text(
        l10n.format_value("add-book-select-price"),
        reply_markup=create_price_keyboard(l10n),
    )
    await state.set_state(AddBook.select_price)
    await call.answer()


@add_book_step_7_router.callback_query(
    StateFilter(AddBook.add_files), F.data == "clear"
)
async def add_book_step_7_clear(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_text(
        l10n.format_value("add-book-prompt-files"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    files = []
    await state.update_data(files=files)
    await call.answer()
