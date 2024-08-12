from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from tgbot.keyboards.inline.buttons import (
    article_button,
    title_button,
    authors_button,
    description_button,
    genres_button,
    cover_button,
    files_button,
    price_edit_button,
)


def edit_book_keyboard(l10n: FluentLocalization, id_book: int) -> InlineKeyboardMarkup:
    """
    The "Edit book" keyboard is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book).
    :return: The "Edit book" keyboard.
    """

    edit_book_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                article_button(l10n, id_book=id_book),
                title_button(l10n, id_book=id_book),
            ],
            [
                authors_button(l10n, id_book=id_book),
                description_button(l10n, id_book=id_book),
            ],
            [
                genres_button(l10n, id_book=id_book),
                cover_button(l10n, id_book=id_book),
            ],
            [
                files_button(l10n, id_book=id_book),
                price_edit_button(l10n, id_book=id_book),
            ],
        ],
    )
    return edit_book_markup
