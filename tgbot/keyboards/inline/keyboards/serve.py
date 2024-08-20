from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from tgbot.keyboards.inline.buttons import serve_button, unavailable_button


def serve_keyboard(l10n: FluentLocalization, id_booking: int) -> InlineKeyboardMarkup:
    """
    The "serve" keyboard is formed.
    :param l10n: Language set by the user.
    :param id_booking: Unique booking identifier.
    :return: The "serve" keyboard.
    """

    serve_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                serve_button(l10n, id_booking=id_booking),
                unavailable_button(l10n),
            ]
        ],
    )
    return serve_markup
