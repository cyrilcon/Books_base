from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from api.books_base_api.schemas import UserSchema
from tg_bot.config import config
from tg_bot.keyboards.inline import channel_keyboard, my_books_keyboard
from tg_bot.services import generate_book_caption

command_my_books_router = Router()


@command_my_books_router.message(
    Command("my_books"),
    flags={"safe_message": False},
)
async def my_books(
    message: Message,
    l10n: FluentLocalization,
    user: UserSchema,
):
    if user.is_premium:
        await message.answer(
            l10n.format_value(
                "my-books-user-has-premium",
                {"channel_link": config.channel.link},
            ),
            reply_markup=channel_keyboard(l10n),
        )
        return

    response = await api.users.get_book_ids(id_user=user.id_user)
    book_ids = response.result

    if len(book_ids) == 0:
        await message.answer(
            l10n.format_value(
                "my-books-no-books",
                {"channel_link": config.channel.link},
            ),
            reply_markup=channel_keyboard(l10n),
        )
        return

    response = await api.books.get_book_by_id(id_book=book_ids[0])
    book = response.get_model()

    caption = await generate_book_caption(
        book_data=book,
        l10n=l10n,
        user=user,
    )
    await message.answer_photo(
        photo=book.cover,
        caption=caption,
        reply_markup=my_books_keyboard(
            l10n=l10n,
            book_ids=book_ids,
        ),
    )
