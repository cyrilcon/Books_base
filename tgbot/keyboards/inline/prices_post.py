from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def prices_post_keyboard(l10n) -> InlineKeyboardMarkup:
    """
    Формируются кнопки "85₽", "50₽", "Не публиковать", "Не от пользователя", "« Назад" и "Отмена".
    :param l10n: Язык установленный у пользователя.
    :return: Кнопки "85₽", "50₽", "Не публиковать", "Не от пользователя", "« Назад" и "Отмена".
    """

    prices_post_buttons = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(text="85₽", callback_data="85"),
                InlineKeyboardButton(text="50₽", callback_data="50"),
            ],
            [
                InlineKeyboardButton(
                    text=l10n.format_value("button-do-not-publish"),
                    callback_data="do_not_publish",
                ),
                InlineKeyboardButton(
                    text=l10n.format_value("button-not-from-a-user"),
                    callback_data="not_from_a_user",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=l10n.format_value("button-back"),
                    callback_data="back",
                ),
                InlineKeyboardButton(
                    text=l10n.format_value("button-cancel"),
                    callback_data="cancel",
                ),
            ],
        ],
    )
    return prices_post_buttons
