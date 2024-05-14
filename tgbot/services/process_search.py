from aiogram.exceptions import TelegramBadRequest

from infrastructure.books_base_api import api
from tgbot.keyboards.inline import pagination_keyboard
from tgbot.services import levenshtein_search


async def process_search(message, l10n, page, title_from_message=None):
    """
    Общая функция для обработки поиска книг и нажатий на кнопки вперед/назад.
    :param message: Объект сообщения или коллбэка.
    :param l10n: Язык установленный у пользователя.
    :param page: Номер текущей страницы.
    :param title_from_message: Название книги из сообщения.
    """

    if title_from_message is None:
        title_from_message = message.text

    response = await api.books.get_all_titles()
    all_titles = response.result["titles"]

    founded_titles = await levenshtein_search(title_from_message.lower(), all_titles)

    response = await api.books.get_books_by_titles(founded_titles)
    status = response.status
    books = response.result

    if status == 200:
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
            # reply_markup=pagination_keyboard(books, page)  # TODO: Добавит клавиатуру с поиском по жанру или автору
        )
