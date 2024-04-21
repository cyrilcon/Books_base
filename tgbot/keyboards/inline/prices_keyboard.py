from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

prices_buttons = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="50₽", callback_data="50"),
            InlineKeyboardButton(text="85₽", callback_data="85"),
        ],
        [
            InlineKeyboardButton(text="Не публиковать", callback_data="do_not_publish"),
            InlineKeyboardButton(
                text="Не от пользователя", callback_data="not_from_a_user"
            ),
        ],
        [
            InlineKeyboardButton(text="« Назад", callback_data="back"),
            InlineKeyboardButton(text="Отмена", callback_data="cancel"),
        ],
    ],
)
