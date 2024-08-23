from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.keyboards.inline import (
    search_by_author_and_genre_keyboard,
    pagination_keyboard,
)
from tgbot.services import generate_book_caption, Messenger


async def search_book_process(
    message: Message,
    l10n: FluentLocalization,
    bot: Bot,
    page: int = 1,
    title_request: str = None,
):
    """
    A common function for handling book searches and forward/backward button presses.
    :param message: Message or callback object.
    :param l10n: Language set by the user.
    :param bot: Bot instance.
    :param page: Page number for pagination.
    :param title_request: Title of the book to search for.
    """

    if title_request is None:
        title_request = message.text

    title_request.replace('"', "")

    if len(title_request) > 255:
        await message.answer(
            l10n.format_value("search-title-too-long"),
            reply_markup=search_by_author_and_genre_keyboard(l10n),
        )
        return

    response = await api.books.search_books_by_title(title_request, page=page)
    result = response.result
    found = result["found"]
    books = result["books"]

    if found == 0:
        await message.answer(
            l10n.format_value("search-not-found", {"title_request": title_request}),
            reply_markup=search_by_author_and_genre_keyboard(l10n),
        )
        return

    if found == 1:
        book = books[0]
        caption = await generate_book_caption(book_data=book, l10n=l10n)

        await Messenger.safe_send_message(
            bot=bot,
            user_id=message.from_user.id,
            text=caption,
            photo=book["cover"],
            # reply_markup=deep_link_buy_keyboard(deep_link),  # TODO: добавить кнопку "Купить"
        )
        return

    text = l10n.format_value("search-found", {"title_request": title_request})
    num = ((page - 1) * 5) + 1

    for book in books:
        book = book["book"]

        article = "#{:04d}".format(book["id_book"])
        title = book["title"]
        authors = book["authors"]
        text += (
            f"\n\n<b>{num}.</b> <code>{title}</code>\n"
            f"{', '.join(f'<code>{author['author'].title()}</code>' for author in authors)}"
            f" (<code>{article}</code>)"
        )
        num += 1

    try:
        await message.edit_text(
            text, reply_markup=pagination_keyboard(l10n, found, books, page)
        )
    except TelegramBadRequest:
        await message.answer(
            text, reply_markup=pagination_keyboard(l10n, found, books, page)
        )
