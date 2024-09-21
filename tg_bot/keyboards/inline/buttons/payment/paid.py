from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def paid_button(
    l10n: FluentLocalization,
    currency: str,
    price: int | float,
    id_payment: str,
) -> InlineKeyboardButton:
    """
    The "Paid" button is formed.
    :param l10n: Language set by the user.
    :param currency: Currency in which the payment was made.
    :param price: Product price.
    :param id_payment: Unique payment identifier.
    :return: The "Paid" button.
    """

    paid = InlineKeyboardButton(
        text=l10n.format_value("button-paid"),
        callback_data=f"premium_paid:{currency}:{price}:{id_payment}",
    )
    return paid
