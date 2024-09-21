from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def pay_stars_button(l10n: FluentLocalization, price: int) -> InlineKeyboardButton:
    """
    The "Pay stars" button is formed.
    :param l10n: Language set by the user.
    :param price: Product price.
    :return: The "Pay stars" button.
    """

    pay_stars = InlineKeyboardButton(
        text=l10n.format_value("button-pay-stars", {"price": price}),
        pay=True,
    )
    return pay_stars
