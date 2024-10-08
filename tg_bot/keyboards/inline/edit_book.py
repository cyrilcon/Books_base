from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline.buttons import (
    edit_article_button,
    edit_title_button,
    edit_authors_button,
    edit_description_button,
    edit_genres_button,
    edit_cover_button,
    edit_files_button,
    edit_price_button,
)


def edit_book_keyboard(l10n: FluentLocalization, id_book: int) -> InlineKeyboardMarkup:
    """
    The "edit_book" keyboard is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book).
    :return: The "edit_book" keyboard.
    """

    edit_book_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                edit_article_button(l10n, id_book=id_book),
                edit_title_button(l10n, id_book=id_book),
            ],
            [
                edit_authors_button(l10n, id_book=id_book),
                edit_description_button(l10n, id_book=id_book),
            ],
            [
                edit_genres_button(l10n, id_book=id_book),
                edit_cover_button(l10n, id_book=id_book),
            ],
            [
                edit_files_button(l10n, id_book=id_book),
                edit_price_button(l10n, id_book=id_book),
            ],
        ],
    )
    return edit_book_markup
