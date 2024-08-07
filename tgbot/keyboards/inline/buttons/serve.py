from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def serve_button(l10n: FluentLocalization, id_booking: int) -> InlineKeyboardButton:
    """
    The "Serve" button is formed.
    :param l10n: Language set by the user.
    :param id_booking: Unique booking identifier.
    :return: The "Serve" button.
    """

    serve = InlineKeyboardButton(
        text=l10n.format_value("button-serve"),
        callback_data=f"serve:{id_booking}",
    )
    return serve
