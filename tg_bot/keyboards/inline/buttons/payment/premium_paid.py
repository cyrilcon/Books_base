from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def premium_paid_button(
    l10n: FluentLocalization,
    price: int | float,
    id_payment: str,
) -> InlineKeyboardButton:
    """
    The "Paid" button is formed.
    :param l10n: Language set by the user.
    :param price: Product price.
    :param id_payment: Unique payment identifier.
    :return: The "Paid" button.
    """

    premium_paid = InlineKeyboardButton(
        text=l10n.format_value("button-paid"),
        callback_data=f"premium_paid:{price}:{id_payment}",
    )
    return premium_paid
