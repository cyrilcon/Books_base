from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def pay_xtr_button(l10n: FluentLocalization, price: int) -> InlineKeyboardButton:
    """
    The "Pay" button is formed.
    :param l10n: Language set by the user.
    :param price: Product price.
    :return: The "Pay" button.
    """

    pay_xtr = InlineKeyboardButton(
        text=l10n.format_value("button-pay-xtr", {"price": price}),
        pay=True,
    )
    return pay_xtr
