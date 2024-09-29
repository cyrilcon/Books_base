from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline.buttons import cancel_button, back_button


def back_cancel_keyboard(l10n: FluentLocalization) -> InlineKeyboardMarkup:
    """
    The "back_cancel" keyboard is formed.
    :param l10n: Language set by the user.
    :return: The "back_cancel" keyboard.
    """

    back_cancel_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                back_button(l10n),
                cancel_button(l10n),
            ]
        ],
    )
    return back_cancel_markup
