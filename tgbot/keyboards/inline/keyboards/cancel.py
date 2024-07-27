from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from tgbot.keyboards.inline.buttons import cancel_button


def cancel_keyboard(l10n: FluentLocalization) -> InlineKeyboardMarkup:
    """
    The "Cancel" keyboard is formed.
    :param l10n: Language set by the user.
    :return: The "Cancel" keyboard.
    """

    cancel_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                cancel_button(l10n),
            ]
        ],
    )
    return cancel_markup
