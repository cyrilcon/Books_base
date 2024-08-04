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
from tgbot.services import ClearKeyboard
from tgbot.states import AddBook

add_book_router_6 = Router()
add_book_router_6.message.filter(AdminFilter())


@add_book_router_6.callback_query(StateFilter(AddBook.add_cover), F.data == "back")
async def back_to_add_book_5(
    call: CallbackQuery, l10n: FluentLocalization, state: FSMContext
):
    """
    Going back to adding genres.
    :param call: Pressed "Back" button.
    :param l10n: Language set by the user.
    :param state: FSM (AddBook).
    """

    await call.answer(cache_time=1)

    data = await state.get_data()
    genres = data.get("genres")
    ready_made_genres = " ".join(["#" + genre["genre"] for genre in genres])

    await call.message.edit_text(
        l10n.format_value(
            "add-book-genres-more",
            {"ready_made_genres": ready_made_genres},
        ),
        reply_markup=done_clear_back_cancel_keyboard(l10n),
    )
    await state.set_state(AddBook.add_genres)


@add_book_router_6.message(StateFilter(AddBook.add_cover), F.photo)
async def add_book_6(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    """
    Adding cover.
    :param message: A message with the expected cover photo of the book.
    :param l10n: Language set by the user.
    :param state: FSM (AddBook).
    :param storage: Storage for FSM.
    :return: Message to add files and go to FSM (add_files).
    """

    await ClearKeyboard.clear(message, storage)

    cover = message.photo[-1].file_id

    sent_message = await message.answer(
        l10n.format_value("add-book-files"),
        reply_markup=back_cancel_keyboard(l10n),
    )

    await state.update_data(cover=cover)
    await state.set_state(AddBook.add_files)

    await ClearKeyboard.safe_message(
        storage=storage,
        user_id=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )
