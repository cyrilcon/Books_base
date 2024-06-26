from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def check_booking_pagination_keyboard(
    position: int, count: int
) -> InlineKeyboardMarkup:
    """
    Формируется клавиатура с пагинацией для просмотра заказов.
    :param position: Позиция заказа среди всего числа заказов.
    :param count: Число всех заказов.
    :return: Клавиатура с пагинацией для просмотра заказов.
    """

    action_buttons = []

    if count > 1:
        if position > 1:
            action_buttons.append(
                InlineKeyboardButton(
                    text=f"⬅️", callback_data=f"booking_page:{position-1}"
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
                    text=f"➡️", callback_data=f"booking_page:{position+1}"
                )
            )

    check_booking_pagination_buttons = InlineKeyboardMarkup(
        inline_keyboard=[action_buttons]
    )

    return check_booking_pagination_buttons
