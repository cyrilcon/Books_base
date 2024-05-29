from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def discounts_keyboard(l10n) -> InlineKeyboardMarkup:
    """
    Формируются кнопки "15%", "30%", "50%" и "Бесплатная книга".
    :param l10n: Язык установленный у пользователя.
    :return: Кнопки "15%", "30%", "50%" и "Бесплатная книга".
    """

    discounts_buttons = InlineKeyboardMarkup(
        row_width=3,
        inline_keyboard=[
            [
                InlineKeyboardButton(text="15%", callback_data="discount_15"),
                InlineKeyboardButton(text="30%", callback_data="discount_30"),
                InlineKeyboardButton(text="50%", callback_data="discount_50"),
            ],
            [
                InlineKeyboardButton(
                    text=l10n.format_value("button-free-book"),
                    callback_data="discount_100",
                )
            ],
        ],
    )
    return discounts_buttons
