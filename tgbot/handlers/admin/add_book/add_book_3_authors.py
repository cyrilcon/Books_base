from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import back_cancel_keyboard
from tgbot.services import ClearKeyboard
from tgbot.states import AddBook

add_book_router_3 = Router()
add_book_router_3.message.filter(AdminFilter())


@add_book_router_3.callback_query(StateFilter(AddBook.add_authors), F.data == "back")
async def back_to_add_book_2(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("add-book-title"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.set_state(AddBook.add_title)


@add_book_router_3.message(StateFilter(AddBook.add_authors), F.text)
async def add_book_3(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    authors = message.text.lower().split(", ")

    for author in authors:
        if len(author) > 255:
            sent_message = await message.answer(
                l10n.format_value("add-book-authors-too-long"),
                reply_markup=back_cancel_keyboard(l10n),
            )
            await ClearKeyboard.safe_message(
                storage=storage,
                user_id=message.from_user.id,
                sent_message_id=sent_message.message_id,
            )
            return

    authors = [{"author": author} for author in authors]

    sent_message = await message.answer(
        l10n.format_value("add-book-description"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.update_data(authors=authors)
    await state.set_state(AddBook.add_description)

    await ClearKeyboard.safe_message(
        storage=storage,
        user_id=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )
