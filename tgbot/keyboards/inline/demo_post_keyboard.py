from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

demo_post_buttons = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Опубликовать", callback_data="post"),
            # InlineKeyboardButton(text="Редактировать", callback_data="edit"),
            InlineKeyboardButton(text="Отмена", callback_data="cancel"),
        ],
    ],
)
