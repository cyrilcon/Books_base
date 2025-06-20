from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def cancel_discount_button(
    l10n: FluentLocalization, discount_value: int
) -> InlineKeyboardButton:
    """
    The "Discount 15%" button is formed.
    :param l10n: Language set by the user.
    :param discount_value: Discount value.
    :return: The "Discount 15%" button.
    """

    cancel_discount = InlineKeyboardButton(
        text=l10n.format_value(
            "button-cancel-discount",
            {"discount_value": discount_value},
        ),
        callback_data=f"cancel_discount",
    )
    return cancel_discount
