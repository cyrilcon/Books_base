from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline.buttons import serve_button, book_unavailable_button


def serve_order_keyboard(
    l10n: FluentLocalization, id_order: int
) -> InlineKeyboardMarkup:
    """
    The "serve_order" keyboard is formed.
    :param l10n: Language set by the user.
    :param id_order: Unique order identifier.
    :return: The "serve_order" keyboard.
    """

    serve_order_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                serve_button(l10n, id_order=id_order),
                book_unavailable_button(l10n, id_order=id_order),
            ]
        ],
    )
    return serve_order_markup
