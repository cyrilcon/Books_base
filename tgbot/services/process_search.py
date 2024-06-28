from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from infrastructure.books_base_api import api
from tgbot.config import Config
from tgbot.keyboards.inline import pagination_keyboard
from . import levenshtein_search, forming_text, safe_send_message, get_user_language


async def process_search(
    config: Config,
    bot: Bot,
    id_user: int,
    message: Message,
    page: int,
    title_from_message: str = None,
):
    """
    Общая функция для обработки поиска книг и нажатий на кнопки вперед/назад.
    :param config: Config с параметрами бота.
    :param bot: Экземпляр бота.
    :param id_user: ID пользователя.
    :param message: Объект сообщения или коллбэка.
    :param page: Номер текущей страницы.
    :param title_from_message: Название книги из сообщения.
    """

    l10n = await get_user_language(id_user)

    if title_from_message is None:
        title_from_message = message.text

    response = await api.books.get_all_titles()
    all_titles = response.result

    founded_titles = await levenshtein_search(title_from_message, all_titles)

    response = await api.books.get_books_by_titles(founded_titles)
    status = response.status
    books = response.result

    if status == 200:
        if len(books) == 1:
            response = await api.books.get_book(books[0]["id_book"])
            book = response.result
            post_text = await forming_text(book, l10n)

            await safe_send_message(
                config=config,
                bot=bot,
                id_user=id_user,
                text=post_text,
                photo=book["cover"],
                # reply_markup=deep_link_buy_keyboard(deep_link),  # TODO: добавить кнопку "Купить"
            )
        else:
            text = l10n.format_value("search-found", {"request": title_from_message})
            num = ((page - 1) * 5) + 1

            start_index = (page - 1) * 5
            end_index = min(page * 5, len(books))

            for item in books[start_index:end_index]:
                article = "#{:04d}".format(item["id_book"])
                title = item["title"]
                authors = item["authors"]
                text += (
                    f"\n\n<b>{num}.</b> <code>{title}</code>\n"
                    f"{', '.join(f'<code>{author['author'].title()}</code>' for author in authors)}"
                    f" (<code>{article}</code>)"
                )
                num += 1

            try:
                await message.edit_text(
                    f"{text}", reply_markup=pagination_keyboard(books, page)
                )
            except TelegramBadRequest:
                await message.answer(
                    f"{text}", reply_markup=pagination_keyboard(books, page)
                )
    elif status == 404:
        await message.answer(
            l10n.format_value("search-not-found", {"request": title_from_message}),
            # reply_markup=pagination_keyboard(books, page)  # TODO: Добавить клавиатуру с поиском по жанру или автору
        )
