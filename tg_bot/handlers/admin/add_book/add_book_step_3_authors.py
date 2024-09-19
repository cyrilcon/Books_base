from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import back_cancel_keyboard
from tg_bot.services import ClearKeyboard
from tg_bot.states import AddBook

add_book_step_3_router = Router()


@add_book_step_3_router.callback_query(
    StateFilter(AddBook.add_authors), F.data == "back"
)
async def back_to_add_book_step_2(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_text(
        l10n.format_value("add-book-prompt-title"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.set_state(AddBook.add_title)
    await call.answer()


@add_book_step_3_router.message(StateFilter(AddBook.add_authors), F.text)
async def add_book_step_3(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    authors = message.text.split(", ")

    for author_name in authors:
        if len(author_name) > 255:
            sent_message = await message.answer(
                l10n.format_value("add-book-error-author-name-too-long"),
                reply_markup=back_cancel_keyboard(l10n),
            )
            await ClearKeyboard.safe_message(
                storage=storage,
                id_user=message.from_user.id,
                sent_message_id=sent_message.message_id,
            )
            return

    authors = [{"author_name": author_name} for author_name in authors]

    sent_message = await message.answer(
        l10n.format_value("add-book-prompt-description"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.update_data(authors=authors)
    await state.set_state(AddBook.add_description)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )
