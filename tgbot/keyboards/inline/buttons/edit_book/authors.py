from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def authors_button(l10n: FluentLocalization, id_book: int) -> InlineKeyboardButton:
    """
    The "Authors" button is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book).
    :return: The "Authors" button.
    """

    authors = InlineKeyboardButton(
        text=l10n.format_value("button-authors"),
        callback_data=f"edit_authors:{id_book}",
    )
    return authors
