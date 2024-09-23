from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def paid_premium_button(
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

    paid_premium = InlineKeyboardButton(
        text=l10n.format_value("button-paid"),
        callback_data=f"paid:premium:{price}:{id_payment}",
    )
    return paid_premium
