from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import back_cancel_keyboard
from tg_bot.states import AddBook

add_book_step_3_router = Router()


@add_book_step_3_router.callback_query(
    StateFilter(AddBook.add_authors),
    F.data == "back",
)
async def back_to_add_book_step_2(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    data = await state.get_data()
    title = data.get("title")

    await call.message.edit_text(
        l10n.format_value(
            "add-book-title-back",
            {"title": title},
        ),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.set_state(AddBook.add_title)
    await call.answer()


@add_book_step_3_router.message(
    StateFilter(AddBook.add_authors),
    F.text,
)
async def add_book_step_3(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    authors = message.text.split(", ")

    for author_name in authors:
        if len(author_name) > 255:
            await message.answer(
                l10n.format_value("add-book-error-author-name-too-long"),
                reply_markup=back_cancel_keyboard(l10n),
            )
            return

        if '"' in author_name:
            await message.answer(
                l10n.format_value("add-book-error-invalid-author-name"),
                reply_markup=back_cancel_keyboard(l10n),
            )
            return

    authors = [{"author_name": author_name} for author_name in authors]

    await message.answer(
        l10n.format_value("add-book-description"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.update_data(authors=authors)
    await state.set_state(AddBook.add_description)
