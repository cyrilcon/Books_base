from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def article_button(l10n: FluentLocalization, id_book: int) -> InlineKeyboardButton:
    """
    The "Article" button is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book).
    :return: The "Article" button.
    """

    article = InlineKeyboardButton(
        text=l10n.format_value("button-article"),
        callback_data=f"article:{id_book}",
    )
    return article
