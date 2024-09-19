from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import (
    back_cancel_keyboard,
    done_clear_back_cancel_keyboard,
)
from tg_bot.services import ClearKeyboard, BookFormatter
from tg_bot.states import AddBook

add_book_step_6_router = Router()


@add_book_step_6_router.callback_query(StateFilter(AddBook.add_cover), F.data == "back")
async def back_to_add_book_step_5(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    data = await state.get_data()
    genres = data.get("genres")
    genres = BookFormatter.format_genres(genres)

    await call.message.edit_text(
        l10n.format_value(
            "add-book-prompt-more-genres",
            {"genres": genres},
        ),
        reply_markup=done_clear_back_cancel_keyboard(l10n),
    )
    await state.set_state(AddBook.add_genres)
    await call.answer()


@add_book_step_6_router.message(StateFilter(AddBook.add_cover), F.photo)
async def add_book_step_6(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    cover = message.photo[-1].file_id

    sent_message = await message.answer(
        l10n.format_value("add-book-prompt-files"),
        reply_markup=back_cancel_keyboard(l10n),
    )

    await state.update_data(cover=cover)
    await state.set_state(AddBook.add_files)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )
