from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def exchange_base_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Exchange base" button is formed.
    :param l10n: Language set by the user.
    :return: The "Exchange base" button.
    """

    exchange_base = InlineKeyboardButton(
        text=l10n.format_value("button-exchange-base"),
        callback_data="exchange_base",
    )
    return exchange_base
