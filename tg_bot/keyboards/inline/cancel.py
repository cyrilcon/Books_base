from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline.buttons import cancel_button


def cancel_keyboard(l10n: FluentLocalization) -> InlineKeyboardMarkup:
    """
    The "cancel" keyboard is formed.
    :param l10n: Language set by the user.
    :return: The "cancel" keyboard.
    """

    cancel_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                cancel_button(l10n),
            ]
        ],
    )
    return cancel_markup
