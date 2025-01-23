from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import (
    back_cancel_keyboard,
    done_clear_back_cancel_keyboard,
)
from tg_bot.services.data import BookFormatter
from tg_bot.states import AddBook

add_book_step_4_router = Router()


@add_book_step_4_router.callback_query(
    StateFilter(AddBook.add_description),
    F.data == "back",
)
async def back_to_add_book_step_3(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    data = await state.get_data()
    authors = BookFormatter.format_authors(data.get("authors"))

    await call.message.edit_text(
        l10n.format_value(
            "add-book-authors-back",
            {"authors": authors},
        ),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.set_state(AddBook.add_authors)
    await call.answer()


@add_book_step_4_router.message(
    StateFilter(AddBook.add_description),
    F.text,
)
async def add_book_step_4(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    description = message.text

    if len(description) > 850:
        await message.answer(
            l10n.format_value("add-book-error-description-too-long"),
            reply_markup=back_cancel_keyboard(l10n),
        )
        return

    data = await state.get_data()
    genres = data.get("genres")

    if genres:
        genres = BookFormatter.format_genres(genres)
        await message.answer(
            l10n.format_value(
                "add-book-more-genres",
                {"genres": genres},
            ),
            reply_markup=done_clear_back_cancel_keyboard(l10n),
        )
    else:
        await message.answer(
            l10n.format_value("add-book-genres"),
            reply_markup=back_cancel_keyboard(l10n),
        )

    await state.update_data(description=description)
    await state.set_state(AddBook.add_genres)
