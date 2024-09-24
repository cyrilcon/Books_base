from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from fluent.runtime import FluentLocalization

from tg_bot.api.books_base_api import api
from tg_bot.config import config
from tg_bot.keyboards.inline import channel_keyboard
from tg_bot.keyboards.inline.keyboards import my_books_keyboard
from tg_bot.services import generate_book_caption

my_books_router = Router()


@my_books_router.message(Command("my_books"))
async def my_books(message: Message, l10n: FluentLocalization):
    id_user = message.from_user.id

    response = await api.users.get_book_ids(id_user=id_user)
    book_ids = response.result

    if len(book_ids) == 0:
        await message.answer(
            l10n.format_value("my-books-no-books"),
            reply_markup=channel_keyboard(l10n),
        )
        return

    response = await api.users.get_user_by_id(id_user=id_user)
    user = response.get_model()

    if user.is_premium:
        await message.answer(
            l10n.format_value(
                "my-books-user-has-premium",
                {"channel_link": config.channel.link},
            ),
            reply_markup=channel_keyboard(l10n),
        )
        return

    response = await api.books.get_book_by_id(book_ids[0])
    book = response.get_model()
    caption = await generate_book_caption(book_data=book, l10n=l10n)

    await message.answer_photo(
        photo=book.cover,
        caption=caption,
        reply_markup=my_books_keyboard(
            l10n=l10n,
            book_ids=book_ids,
        ),
    )


@my_books_router.callback_query(F.data.startswith("my_books_page"))
async def my_books_page(call: CallbackQuery, l10n: FluentLocalization):
    page = int(call.data.split(":")[-1])
    id_user = call.from_user.id

    response = await api.users.get_user_by_id(id_user=id_user)
    user = response.get_model()

    if user.is_premium:
        await call.message.edit_reply_markup()
        await call.answer(
            l10n.format_value("my-books-user-has-premium-alert"),
            show_alert=True,
        )
        await call.answer()
        return

    response = await api.users.get_book_ids(id_user=id_user)
    book_ids = response.result

    response = await api.books.get_book_by_id(book_ids[page - 1])
    book = response.get_model()

    caption = await generate_book_caption(book_data=book, l10n=l10n)

    await call.message.edit_media(
        media=InputMediaPhoto(media=book.cover, caption=caption),
        reply_markup=my_books_keyboard(
            l10n=l10n,
            book_ids=book_ids,
            page=page,
        ),
    )
    await call.answer()
