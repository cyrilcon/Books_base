from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline.buttons import done_button, cancel_button


def formats_keyboard(
    l10n: FluentLocalization,
    formats: List[str],
) -> InlineKeyboardMarkup:
    """
    The keyboard with file formats for deletion.
    :param l10n: Language set by the user.
    :param formats: List of book formats.
    :return: The keyboard with file formats for deletion.
    """

    formats_buttons = []

    for i in range(0, len(formats), 3):
        row = []
        for file_format in formats[i : i + 3]:
            row.append(
                InlineKeyboardButton(
                    text=file_format,
                    callback_data=f"delete_format:{file_format}",
                )
            )
        formats_buttons.append(row)

    formats_buttons.append(
        [
            done_button(l10n),
            cancel_button(l10n),
        ]
    )

    formats_buttons_markup = InlineKeyboardMarkup(inline_keyboard=formats_buttons)
    return formats_buttons_markup
