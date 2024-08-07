from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from fluent.runtime import FluentLocalization

from tgbot.keyboards.inline.buttons import serve_button


def check_booking_keyboard(
    l10n: FluentLocalization,
    id_booking: int,
    count: int,
    position: int = 1,
) -> InlineKeyboardMarkup:
    """
    A keyboard with pagination for viewing orders is formed.
    :param l10n: Language set by the user.
    :param id_booking: Unique booking identifier.
    :param count: Number of all orders.
    :param position: Order position among the total number of orders.
    :return: Keyboard with pagination for viewing orders.
    """

    action_buttons = []

    if count > 1:
        if position > 1:
            action_buttons.append(
                InlineKeyboardButton(
                    text=f"⬅️", callback_data=f"booking_position:{position-1}"
                )
            )

        action_buttons.append(
            InlineKeyboardButton(
                text=f"{position}/{count}", callback_data=f"booking_pagination"
            )
        )

        if position < count:
            action_buttons.append(
                InlineKeyboardButton(
                    text=f"➡️", callback_data=f"booking_position:{position+1}"
                )
            )

    check_booking_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                serve_button(l10n, id_booking=id_booking),
            ],
            action_buttons,
        ]
    )

    return check_booking_markup
