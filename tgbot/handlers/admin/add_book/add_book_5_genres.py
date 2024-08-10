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
)
from tgbot.services import ClearKeyboard, genres_to_list
from tgbot.states import AddBook

add_book_router_5 = Router()
add_book_router_5.message.filter(AdminFilter())


@add_book_router_5.callback_query(StateFilter(AddBook.add_genres), F.data == "back")
async def back_to_add_book_4(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("add-book-description"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.set_state(AddBook.add_description)


@add_book_router_5.message(StateFilter(AddBook.add_genres), F.text)
async def add_book_5(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    genres_from_message = message.text

    data = await state.get_data()
    genres = data.get("genres")

    genres, too_long_genres = await genres_to_list(genres_from_message, genres)
    if too_long_genres:
        sent_message = await message.answer(
            l10n.format_value("genres-too-long"),
            reply_markup=back_cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            user_id=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    await state.update_data(genres=genres)
    ready_made_genres = " ".join(["#" + genre["genre"] for genre in genres])

    sent_message = await message.answer(
        l10n.format_value(
            "add-book-genres-more",
            {"genres": ready_made_genres},
        ),
        reply_markup=done_clear_back_cancel_keyboard(l10n),
    )
    await ClearKeyboard.safe_message(
        storage=storage,
        user_id=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@add_book_router_5.callback_query(StateFilter(AddBook.add_genres), F.data == "done")
async def done_add_book_5(
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


@add_book_router_5.callback_query(StateFilter(AddBook.add_genres), F.data == "clear")
async def clear_add_book_5(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("add-book-genres"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    genres = []
    await state.update_data(genres=genres)
