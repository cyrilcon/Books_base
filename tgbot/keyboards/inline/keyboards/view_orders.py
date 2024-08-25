from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from fluent.runtime import FluentLocalization

from tgbot.keyboards.inline.buttons import serve_button, unavailable_button


def view_orders_keyboard(
    l10n: FluentLocalization,
    id_order: int,
    orders_count: int,
    position: int = 1,
) -> InlineKeyboardMarkup:
    """
    A keyboard with pagination for viewing orders is formed.
    :param l10n: Language set by the user.
    :param id_order: Unique order identifier.
    :param orders_count: Number of all orders.
    :param position: Order position in the database.
    :return: Keyboard with pagination for viewing orders.
    """

    action_buttons = []

    if orders_count > 1:
        if position > 1:
            action_buttons.append(
                InlineKeyboardButton(
                    text=f"⬅️", callback_data=f"order_position:{position-1}"
                )
            )

        action_buttons.append(
            InlineKeyboardButton(
                text=f"{l10n.format_value("page")} {position}/{orders_count}",
                callback_data=f"order_position_info",
            )
        )

        if position < orders_count:
            action_buttons.append(
                InlineKeyboardButton(
                    text=f"➡️", callback_data=f"order_position:{position+1}"
                )
            )

    view_orders_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                serve_button(l10n, id_order=id_order),
                unavailable_button(l10n, id_order=id_order),
            ],
            action_buttons,
        ]
    )

    return view_orders_markup
