from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from tgbot.keyboards.inline.buttons import serve_button, unavailable_button


def serve_unavailable_keyboard(
    l10n: FluentLocalization, id_booking: int
) -> InlineKeyboardMarkup:
    """
    The "Serve" and "Unavailable" keyboard is formed.
    :param l10n: Language set by the user.
    :param id_booking: Unique booking identifier.
    :return: The "Serve" and "Unavailable" keyboard.
    """

    serve_unavailable_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                serve_button(l10n, id_booking=id_booking),
                unavailable_button(l10n),
            ]
        ],
    )
    return serve_unavailable_markup
