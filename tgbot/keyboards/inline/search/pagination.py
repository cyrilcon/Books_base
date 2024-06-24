from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def pagination_keyboard(books: list, page: int = 1) -> InlineKeyboardMarkup:
    """
    Формируется клавиатура с пагинацией.
    :param books: Список с книгами.
    :param page: Номер текущей страницы.
    :return: Клавиатура с пагинацией.
    """

    buttons = []
    num = ((page - 1) * 5) + 1
    start_index = (page - 1) * 5
    end_index = min(page * 5, len(books))

    for book in books[start_index:end_index]:
        id_book = "#{:04d}".format(book["id_book"])
        id_book_button = InlineKeyboardButton(
            text=f"{num}", callback_data=f"id_book={id_book}"
        )
        buttons.append(id_book_button)
        num += 1

    bottom_buttons = []

    if page > 1:
        bottom_buttons.append(
            InlineKeyboardButton(text=f"⬅️", callback_data=f"page:{page-1}")
        )

    if len(books) > 5:
        all_pages = (len(books) + 4) // 5
        bottom_buttons.append(
            InlineKeyboardButton(
                text=f"{page}/{all_pages}",
                callback_data=f"pagination_info:{page}:{all_pages}",
            )
        )

        if end_index < len(books):
            bottom_buttons.append(
                InlineKeyboardButton(text=f"➡️", callback_data=f"page:{page+1}")
            )

    pagination_buttons = InlineKeyboardMarkup(
        row_width=5, inline_keyboard=[buttons, bottom_buttons]
    )

    return pagination_buttons
