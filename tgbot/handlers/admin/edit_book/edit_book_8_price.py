from aiogram import Router, F
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.keyboards.inline import update_price_keyboard, edit_book_keyboard
from tgbot.services import generate_book_caption

edit_price_router = Router()


@edit_price_router.callback_query(F.data.startswith("edit_price"))
async def edit_price(call: CallbackQuery, l10n: FluentLocalization):
    id_book = int(call.data.split(":")[-1])
    await call.message.answer(
        l10n.format_value("edit-book-select-price"),
        reply_markup=update_price_keyboard(l10n, id_book),
    )
    await call.answer()


@edit_price_router.callback_query(F.data.startswith("update_price"))
async def update_price(
    call: CallbackQuery,
    l10n: FluentLocalization,
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

    response = await api.books.update_book(id_book_edited, price=price)
    book = response.get_model()

    await call.message.edit_text(l10n.format_value("edit-book-success"))
    await call.message.answer_photo(
        photo=book.cover,
        caption=caption,
        reply_markup=edit_book_keyboard(l10n, book.id_book),
    )
    await call.answer()
