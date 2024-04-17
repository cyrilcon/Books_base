from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

cancel_button = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text="Отмена", callback_data="back_and_CANCEL")]
    ],
)

back_and_cancel_buttons = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="« Назад", callback_data="BACK_and_cancel"),
            InlineKeyboardButton(text="Отмена", callback_data="back_and_CANCEL"),
        ]
    ],
)
