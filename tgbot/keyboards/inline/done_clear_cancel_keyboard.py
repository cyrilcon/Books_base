from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

done_clear_cancel_buttons = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Готово", callback_data="done"),
            InlineKeyboardButton(text="Стереть", callback_data="clear"),
        ],
        [InlineKeyboardButton(text="Отмена", callback_data="cancel")],
    ],
)
