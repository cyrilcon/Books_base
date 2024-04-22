from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def demo_post_keyboard(l10n):
    """
    Формируются кнопки "Опубликовать" и "Отмена".
    :param l10n: Язык установленный у пользователя.
    :return: Кнопки "Опубликовать" и "Отмена".
    """

    demo_post_buttons = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=l10n.format_value("button-post"), callback_data="post"
                ),
                # InlineKeyboardButton(text="Редактировать", callback_data="edit"),
                InlineKeyboardButton(
                    text=l10n.format_value("button-cancel"), callback_data="cancel"
                ),
            ],
        ],
    )
    return demo_post_buttons
