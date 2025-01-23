from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.api_client import api
from tg_bot.keyboards.inline import cancel_keyboard, edit_book_keyboard
from tg_bot.services.data import generate_book_caption
from tg_bot.states import EditBook

edit_description_router = Router()


@edit_description_router.callback_query(
    F.data.startswith("edit_description"),
    flags={"skip_message": 1},
)
async def edit_description(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    id_book = int(call.data.split(":")[-1])

    response = await api.books.get_book_by_id(id_book=id_book)
    book = response.get_model()

    await call.message.answer(
        l10n.format_value(
            "edit-book-description",
            {"description": book.description},
        ),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.update_data(id_book_edited=id_book)
    await state.set_state(EditBook.edit_description)
    await call.answer()


@edit_description_router.message(
    StateFilter(EditBook.edit_description),
    F.text,
)
async def edit_description_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    description = message.text

    if len(description) > 850:
        await message.answer(
            l10n.format_value("edit-book-error-description-too-long"),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    data = await state.get_data()
    id_book_edited = data.get("id_book_edited")

    response = await api.books.get_book_by_id(id_book=id_book_edited)
    book = response.get_model()

    caption = await generate_book_caption(
        book_data=book,
        l10n=l10n,
        description=description,
    )
    caption_length = len(caption)

    if caption_length > 1024:
        await message.answer(
            l10n.format_value(
                "edit-book-error-caption-too-long",
                {"caption_length": caption_length},
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    response = await api.books.update_book(
        id_book_edited=id_book_edited,
        description=description,
    )
    book = response.get_model()

    await message.answer(l10n.format_value("edit-book-success"))
    await message.answer_photo(
        photo=book.cover,
        caption=caption,
        reply_markup=edit_book_keyboard(l10n, id_book=book.id_book),
    )
    await state.clear()
