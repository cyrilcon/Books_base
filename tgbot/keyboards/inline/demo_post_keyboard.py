from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

demo_post_buttons = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Опубликовать", callback_data="done"),
            InlineKeyboardButton(text="Редактировать", callback_data="clear"),
        ],
        [InlineKeyboardButton(text="Отмена", callback_data="cancel")],
    ],
)
