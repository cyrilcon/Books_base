from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.keyboards.inline import (
    back_cancel_keyboard,
    done_clear_back_cancel_keyboard,
)
from tgbot.services import ClearKeyboard, BookFormatter
from tgbot.states import AddBook

add_book_step_4_router = Router()


@add_book_step_4_router.callback_query(
    StateFilter(AddBook.add_description), F.data == "back"
)
async def back_to_add_book_step_3(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_text(
        l10n.format_value("add-book-prompt-authors"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.set_state(AddBook.add_authors)
    await call.answer()


@add_book_step_4_router.message(StateFilter(AddBook.add_description), F.text)
async def add_book_step_4(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    description = message.text

    if len(description) > 850:
        sent_message = await message.answer(
            l10n.format_value("add-book-error-description-too-long"),
            reply_markup=back_cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    data = await state.get_data()
    genres = data.get("genres")

    if genres:
        genres = BookFormatter.format_genres(genres)
        sent_message = await message.answer(
            l10n.format_value(
                "add-book-prompt-more-genres",
                {"genres": genres},
            ),
            reply_markup=done_clear_back_cancel_keyboard(l10n),
        )
    else:
        sent_message = await message.answer(
            l10n.format_value("add-book-prompt-genres"),
            reply_markup=back_cancel_keyboard(l10n),
        )

    await state.update_data(description=description)
    await state.set_state(AddBook.add_genres)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )
