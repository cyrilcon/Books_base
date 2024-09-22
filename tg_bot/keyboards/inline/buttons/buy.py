from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization

from tg_bot.api.books_base_api import api


async def buy_button(l10n: FluentLocalization, id_book: int) -> InlineKeyboardButton:
    """
    The "Buy" button is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book).
    :return: The "Buy" button.
    """

    response = await api.books.get_book_by_id(id_book)
    book = response.get_model()

    buy = InlineKeyboardButton(
        text=l10n.format_value("button-buy"),
        callbuy_data=f"buy:{book.price}:{id_book}",
    )
    return buy
