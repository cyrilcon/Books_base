from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def orders_keyboard(orders: List[int]) -> InlineKeyboardMarkup:
    """
    The keyboard with order numbers.
    :param orders: List of orders.
    :return: The keyboard with file order numbers.
    """

    orders_buttons = []

    for i in range(0, len(orders), 3):
        row = []
        for order_number in orders[i : i + 3]:
            row.append(
                InlineKeyboardButton(
                    text=str(order_number),
                    callback_data=f"cancel_order:{order_number}",
                )
            )
        orders_buttons.append(row)

    orders_buttons_markup = InlineKeyboardMarkup(inline_keyboard=orders_buttons)

    return orders_buttons_markup
