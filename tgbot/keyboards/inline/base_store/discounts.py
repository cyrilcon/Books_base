from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def discounts_keyboard(l10n) -> InlineKeyboardMarkup:
    """
    Формируются кнопки "15%", "30%", "50%" и "Бесплатная книга".
    :param l10n: Язык установленный у пользователя.
    :return: Кнопки "15%", "30%", "50%" и "Бесплатная книга".
    """

    discounts_buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="15%", callback_data="discount:15:20"),
                InlineKeyboardButton(text="30%", callback_data="discount:30:35"),
                InlineKeyboardButton(text="50%", callback_data="discount:50:45"),
            ],
            [
                InlineKeyboardButton(
                    text=l10n.format_value("button-free-book"),
                    callback_data="discount:100:55",
                )
            ],
        ],
    )
    return discounts_buttons
