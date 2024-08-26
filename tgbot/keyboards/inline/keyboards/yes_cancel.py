from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from tgbot.keyboards.inline.buttons import cancel_button, yes_button


def yes_cancel_keyboard(l10n: FluentLocalization) -> InlineKeyboardMarkup:
    """
    The "yes_cancel" keyboard is formed.
    :param l10n: Language set by the user.
    :return: The "yes_cancel" keyboard.
    """

    yes_cancel_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                yes_button(l10n),
                cancel_button(l10n),
            ]
        ],
    )
    return yes_cancel_markup
