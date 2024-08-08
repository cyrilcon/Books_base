from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def reply_button(
    l10n: FluentLocalization,
    id_user: int | None = None,
) -> InlineKeyboardButton:
    """
    The "Reply" button is formed.
    :param l10n: Language set by the user.
    :param id_user: Unique user identifier.
    :return: The "Reply" button.
    """

    recipient = id_user if id_user else "admin"

    reply = InlineKeyboardButton(
        text=l10n.format_value("button-reply"),
        callback_data=f"reply_to:{recipient}",
    )
    return reply
