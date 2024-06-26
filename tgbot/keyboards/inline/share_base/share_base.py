from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def share_base_keyboard(l10n, bases: int) -> InlineKeyboardMarkup:
    """
    Формируются кнопки для отправки base другому пользователю.
    :param l10n: Язык установленный у пользователя.
    :param bases: Количество base у пользователя.
    :return: Кнопки для отправки base другому пользователю.
    """

    base_amounts = [10, 20, 30, 50, 100]
    buttons = []

    for amount in base_amounts:
        status_icon = "💎" if bases >= amount else "❌"
        buttons.append(
            InlineKeyboardButton(
                text=f"{amount} {status_icon}",
                callback_data=f"share_base:{amount}",
            )
        )

    # Группировка кнопок в строки
    keyboard_buttons = [buttons[:3], buttons[3:]]

    # Добавление кнопки отмены
    cancel_button = InlineKeyboardButton(
        text=l10n.format_value("button-cancel"),
        callback_data="share_base_cancel",
    )
    keyboard_buttons.append([cancel_button])

    share_base_buttons = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    return share_base_buttons
