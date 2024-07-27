from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def done_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Done" button is formed.
    :param l10n: Language set by the user.
    :return: The "Done" button.
    """

    done = InlineKeyboardButton(
        text=l10n.format_value("button-done"),
        callback_data="done",
    )

    return done
