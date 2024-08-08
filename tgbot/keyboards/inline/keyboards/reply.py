from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from tgbot.keyboards.inline.buttons import reply_button


def reply_keyboard(
    l10n: FluentLocalization,
    id_user: int | None = None,
) -> InlineKeyboardMarkup:
    """
    The "Reply" keyboard is formed.
    :param l10n: Language set by the user.
    :param id_user: Unique user identifier.
    :return: The "Reply" keyboard.
    """

    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                reply_button(l10n, id_user=id_user),
            ]
        ],
    )
    return reply_markup
