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
from tgbot.services import ClearKeyboard, formats_to_list
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
    files, text = await formats_to_list(message, l10n, files)

    await state.update_data(files=files)
    sent_message = await message.answer(
        text, reply_markup=done_clear_back_cancel_keyboard(l10n)
    )
    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
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
