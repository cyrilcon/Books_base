import re

from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.api_client import api
from tg_bot.api_client.schemas import UserSchema
from tg_bot.keyboards.inline import buy_or_read_keyboard
from tg_bot.services import BookFormatter, generate_book_caption

start_deep_link_router = Router()


@start_deep_link_router.message(
    CommandStart(deep_link=True, magic=F.args.regexp(re.compile(r"book_(\d+)"))),
    flags={"safe_message": False},
)
async def start_deep_link(
    message: Message,
    l10n: FluentLocalization,
    command: CommandObject,
    user: UserSchema,
):
    id_book = int(command.args.split("_")[1])

    response = await api.books.get_book_by_id(id_book=id_book)
    status = response.status

    if status != 200:
        article = BookFormatter.format_article(id_book=id_book)

        await message.answer(
            l10n.format_value(
                "error-book-unavailable",
                {"article": article},
            )
        )
        return

    book = response.get_model()

    caption = await generate_book_caption(
        book_data=book,
        l10n=l10n,
        user=user,
    )

    await message.answer_photo(
        photo=book.cover,
        caption=caption,
        reply_markup=await buy_or_read_keyboard(
            l10n=l10n,
            id_book=id_book,
            user=user,
        ),
    )
