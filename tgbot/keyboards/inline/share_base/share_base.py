from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def share_base_keyboard(l10n) -> InlineKeyboardMarkup:
    """
    Формируются кнопки для отправки base другому пользователю.
    :param l10n: Язык установленный у пользователя.
    :return: Кнопки для отправки base другому пользователю.
    """

    share_base_buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="10 💎",
                    callback_data=f"share_base:10",
                ),
                InlineKeyboardButton(
                    text="20 💎",
                    callback_data=f"share_base:20",
                ),
                InlineKeyboardButton(
                    text="30 💎",
                    callback_data=f"share_base:30",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="50 💎",
                    callback_data=f"share_base:50",
                ),
                InlineKeyboardButton(
                    text="100 💎",
                    callback_data=f"share_base:100",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=l10n.format_value("button-cancel"),
                    callback_data=f"share_base_cancel",
                )
            ],
        ],
    )
    return share_base_buttons
