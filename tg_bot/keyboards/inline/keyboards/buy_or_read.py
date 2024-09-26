from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.keyboards.inline.buttons import buy_book_button, read_button


async def buy_or_read_keyboard(
    l10n: FluentLocalization,
    id_book: int,
    id_user: int,
) -> InlineKeyboardMarkup:
    """
    The "buy_or_read" keyboard is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book).
    :param id_user: Unique user identifier.
    :return: The "buy_or_read" keyboard.
    """

    response = await api.users.get_user_by_id(id_user)
    user = response.get_model()

    response = await api.users.get_book_ids(id_user=user.id_user)
    book_ids = response.result

    if user.is_premium or id_book in book_ids:
        button = read_button(l10n, id_book=id_book)
    else:
        button = await buy_book_button(l10n, id_book=id_book)

    buy_or_read_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                button,
            ],
        ],
    )
    return buy_or_read_markup
