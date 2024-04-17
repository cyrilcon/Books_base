from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

done_clear_cancel_buttons = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Готово", callback_data="DONE_clear_cancel"),
            InlineKeyboardButton(text="Стереть", callback_data="done_CLEAR_cancel"),
        ],
        [InlineKeyboardButton(text="Отмена", callback_data="back_and_CANCEL")],
    ],
)
