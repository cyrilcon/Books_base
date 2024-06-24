from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def show_booking_cancel_keyboard(l10n, id_book: int) -> InlineKeyboardMarkup:
    """
    Формируются кнопки "Посмотреть книгу", "Всё равно заказать" и "Отмена".
    :param l10n: Язык установленный у пользователя.
    :param id_book: ID книги.
    :return: Кнопки "Посмотреть книгу", "Всё равно заказать" и "Отмена".
    """

    show_booking_cancel_buttons = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=l10n.format_value("button-show-book"),
                    callback_data=f"show_book:{id_book}",
                ),
                InlineKeyboardButton(
                    text=l10n.format_value("button-booking"), callback_data="booking"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=l10n.format_value("button-cancel"), callback_data="cancel"
                ),
            ],
        ],
    )
    return show_booking_cancel_buttons
