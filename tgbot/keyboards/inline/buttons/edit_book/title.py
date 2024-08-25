from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def title_button(l10n: FluentLocalization, id_book: int) -> InlineKeyboardButton:
    """
    The "Title" button is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book).
    :return: The "Title" button.
    """

    title = InlineKeyboardButton(
        text=l10n.format_value("button-title"),
        callback_data=f"edit_title:{id_book}",
    )
    return title
