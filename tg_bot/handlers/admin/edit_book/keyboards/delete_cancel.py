from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline.buttons import (
    delete_button,
    cancel_button,
)


def delete_cancel_keyboard(l10n: FluentLocalization) -> InlineKeyboardMarkup:
    """
    The "delete_cancel" keyboard is formed.
    :param l10n: Language set by the user.
    :return: The "delete_cancel" keyboard.
    """

    delete_cancel_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                delete_button(l10n),
                cancel_button(l10n),
            ],
        ],
    )
    return delete_cancel_markup
