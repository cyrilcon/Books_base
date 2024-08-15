import re

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.services import search_book_process, generate_book_caption, Messenger

search_by_title_router = Router()


@search_by_title_router.message(F.text, flags={"chat_action": "typing"})
async def search_by_title(
    message: Message,
    l10n: FluentLocalization,
    bot: Bot,
):
    await search_book_process(message, l10n, bot)


@search_by_title_router.callback_query(F.data.startswith("page"))
async def search_by_title_pagination(
    call: CallbackQuery,
    l10n: FluentLocalization,
    bot: Bot,
):
    await call.answer(cache_time=1)

    page = int(call.data.split(":")[-1])
    title_request = re.search(r'"([^"]*)"', call.message.text).group(1)

    await search_book_process(call.message, l10n, bot, page, title_request)


@search_by_title_router.callback_query(F.data.startswith("id_book"))
async def search_by_title_get_book(
    call: CallbackQuery,
    l10n: FluentLocalization,
    bot: Bot,
):
    await call.answer(cache_time=1)

    id_book = int(call.data.split(":")[-1])
    response = await api.books.get_book_by_id(id_book)
    status = response.status

    if status == 200:
        book = response.result

        caption = await generate_book_caption(data=book, l10n=l10n)

        await Messenger.safe_send_message(
            bot=bot,
            user_id=call.from_user.id,
            text=caption,
            photo=book["cover"],
            # reply_markup=deep_link_buy_keyboard(deep_link),  # TODO: добавить кнопку "Купить"
        )
    else:
        await call.message.answer(
            l10n.format_value(
                "search-book-does-not-exist",
                {"article": "#{:04d}".format(int(id_book))},
            )
        )
