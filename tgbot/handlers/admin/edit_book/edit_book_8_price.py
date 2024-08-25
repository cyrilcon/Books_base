from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import update_price_keyboard, edit_book_keyboard
from tgbot.services import generate_book_caption, Messenger

edit_book_8_router = Router()
edit_book_8_router.message.filter(AdminFilter())


@edit_book_8_router.callback_query(F.data.startswith("edit_price"))
async def edit_price(call: CallbackQuery, l10n: FluentLocalization):
    await call.answer(cache_time=1)

    id_book = int(call.data.split(":")[-1])

    await call.message.answer(
        l10n.format_value("edit-book-price"),
        reply_markup=update_price_keyboard(l10n, id_book),
    )


@edit_book_8_router.callback_query(F.data.startswith("update_price"))
async def edit_price_process(
    call: CallbackQuery,
    l10n: FluentLocalization,
    bot: Bot,
):
    id_book_edited = int(call.data.split(":")[-1])
    price = int(call.data.split(":")[-2])

    response = await api.books.get_book_by_id(id_book_edited)
    book = response.result

    if price == book["price"]:
        await call.answer(l10n.format_value("edit-book-price-error"), show_alert=True)
        return

    await call.answer(cache_time=1)

    response = await api.books.update_book(id_book_edited, price=price)
    book = response.result

    caption = await generate_book_caption(book_data=book, l10n=l10n)
    caption_length = len(caption)

    if caption_length <= 1024:
        await call.message.edit_text(
            l10n.format_value("edit-book-success"),
            reply_markup=None,
        )
        await Messenger.safe_send_message(
            bot=bot,
            user_id=call.from_user.id,
            text=caption,
            photo=book["cover"],
            reply_markup=edit_book_keyboard(l10n, book["id_book"]),
        )
    else:
        await call.message.answer(
            l10n.format_value(
                "edit-book-error-caption-too-long",
                {"caption_length": caption_length},
            )
        )
