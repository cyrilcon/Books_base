from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def serve_order_button(l10n: FluentLocalization, id_order: int) -> InlineKeyboardButton:
    """
    The "Serve" button is formed.
    :param l10n: Language set by the user.
    :param id_order: Unique order identifier.
    :return: The "Serve" button.
    """

    serve_order = InlineKeyboardButton(
        text=l10n.format_value("button-serve"),
        callback_data=f"serve_order:{id_order}",
    )
    return serve_order
