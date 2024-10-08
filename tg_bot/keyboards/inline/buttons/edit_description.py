from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def edit_description_button(
    l10n: FluentLocalization,
    id_book: int,
) -> InlineKeyboardButton:
    """
    The "Edit description" button is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book).
    :return: The "Edit description" button.
    """

    edit_description = InlineKeyboardButton(
        text=l10n.format_value("button-description"),
        callback_data=f"edit_description:{id_book}",
    )
    return edit_description
