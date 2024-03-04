from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

cancel_button = InlineKeyboardMarkup(row_width=1,  # row_width - количество кнопок в строке
                                     inline_keyboard=[
                                         [
                                             InlineKeyboardButton(
                                                 text="Отмена",
                                                 callback_data="cancel"
                                             )
                                         ]
                                     ])
