from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def cancel_payment_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Cancel payment" button is formed.
    :param l10n: Language set by the user.
    :return: The "Cancel payment" button.
    """

    cancel_payment = InlineKeyboardButton(
        text=l10n.format_value("button-cancel-payment"),
        callback_data=f"cancel_payment",
    )
    return cancel_payment
