from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def edit_authors_button(l10n: FluentLocalization, id_book: int) -> InlineKeyboardButton:
    """
    The "Edit authors" button is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book).
    :return: The "Edit authors" button.
    """

    edit_authors = InlineKeyboardButton(
        text=l10n.format_value("button-edit-authors"),
        callback_data=f"edit_authors:{id_book}",
    )
    return edit_authors
