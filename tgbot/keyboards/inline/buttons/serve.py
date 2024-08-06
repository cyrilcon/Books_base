from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def serve_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Serve" button is formed.
    :param l10n: Language set by the user.
    :return: The "Serve" button.
    """

    serve = InlineKeyboardButton(
        text=l10n.format_value("button-serve"),
        callback_data="serve",
    )
    return serve
