from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def pay_rub_button(
    l10n: FluentLocalization,
    price: float,
    url_payment: str,
) -> InlineKeyboardButton:
    """
    The "Pay" button is formed.
    :param l10n: Language set by the user.
    :param price: Product price.
    :param url_payment: Payment link.
    :return: The "Pay" button.
    """

    pay_rub = InlineKeyboardButton(
        text=l10n.format_value(
            "button-pay-rub",
            {"price": price},
        ),
        url=f"{url_payment}",
    )
    return pay_rub
