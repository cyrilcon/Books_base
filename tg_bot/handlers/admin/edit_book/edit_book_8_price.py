from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.keyboards.inline import edit_price_keyboard, edit_book_keyboard
from tg_bot.services import generate_book_caption
from tg_bot.states import EditBook

edit_price_router = Router()


@edit_price_router.callback_query(
    F.data.startswith("edit_price"),
    flags={"skip_message": 1},
)
async def edit_price(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    id_book = int(call.data.split(":")[-1])
    await call.message.answer(
        l10n.format_value("edit-book-price"),
        reply_markup=edit_price_keyboard(l10n, id_book=id_book),
    )
    await state.set_state(EditBook.edit_price)
    await call.answer()


@edit_price_router.callback_query(
    StateFilter(EditBook.edit_price),
    F.data.startswith("price"),
)
async def update_price(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    id_book_edited = int(call.data.split(":")[-1])
    price = int(call.data.split(":")[-2])

    response = await api.books.get_book_by_id(id_book_edited)
    book = response.get_model()

    if price == book.price:
        await call.answer(
            l10n.format_value("edit-book-price-error-price-already-set"),
            show_alert=True,
        )
        return

    caption = await generate_book_caption(book_data=book, l10n=l10n, price=price)
    caption_length = len(caption)

    if caption_length > 1024:
        await call.answer(
            l10n.format_value(
                "edit-book-error-caption-too-long",
                {"caption_length": caption_length},
            ),
            show_alert=True,
        )
        return

    response = await api.books.update_book(id_book_edited=id_book_edited, price=price)
    book = response.get_model()

    await call.message.edit_text(l10n.format_value("edit-book-success"))
    await call.message.answer_photo(
        photo=book.cover,
        caption=caption,
        reply_markup=edit_book_keyboard(l10n, id_book=book.id_book),
    )
    await state.clear()
    await call.answer()


@edit_price_router.message(
    StateFilter(EditBook.edit_price),
    flags={
        "clear_keyboard": False,
        "safe_message": False,
    },
)
async def edit_price_unprocessed_messages(
    message: Message,
    l10n: FluentLocalization,
):
    await message.answer(l10n.format_value("edit-book-price-unprocessed-messages"))
