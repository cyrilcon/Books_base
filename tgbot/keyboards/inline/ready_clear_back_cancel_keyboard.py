from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ready_clear_back_cancel_buttons = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Готово", callback_data="done"),
            InlineKeyboardButton(text="Стереть", callback_data="clear"),
        ],
        [
            InlineKeyboardButton(text="« Назад", callback_data="back"),
            InlineKeyboardButton(text="Отмена", callback_data="cancel"),
        ],
    ],
)
