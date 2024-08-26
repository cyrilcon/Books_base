import re

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionMiddleware
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.services import search_book_process, generate_book_caption, BookFormatter

search_by_title_router = Router()
search_by_title_router.message.middleware(ChatActionMiddleware())


@search_by_title_router.message(F.text, flags={"chat_action": "typing"})
async def search_by_title(message: Message, l10n: FluentLocalization):
    await search_book_process(message, l10n)


@search_by_title_router.callback_query(F.data.startswith("search_book_page"))
async def search_book_page(call: CallbackQuery, l10n: FluentLocalization):
    page = int(call.data.split(":")[-1])
    book_title_request = re.search(r'"([^"]*)"', call.message.text).group(1)

    await search_book_process(call.message, l10n, page, book_title_request)

    await call.answer()


@search_by_title_router.callback_query(F.data.startswith("id_book"))
async def search_by_title_get_book(call: CallbackQuery, l10n: FluentLocalization):
    await call.answer(cache_time=1)

    id_book = int(call.data.split(":")[-1])
    article = BookFormatter.format_article(id_book)

    response = await api.books.get_book_by_id(id_book)
    status = response.status

    if status == 200:
        book = response.get_model()
        caption = await generate_book_caption(book_data=book, l10n=l10n)

        await call.message.answer_photo(
            photo=book.cover,
            caption=caption,
            # reply_markup=deep_link_buy_keyboard(deep_link),  # TODO: добавить кнопку "Купить"
        )
    else:
        await call.message.answer(
            l10n.format_value(
                "search-by-title-error-book-unavailable",
                {"article": article},
            )
        )
