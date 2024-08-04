from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from tgbot.keyboards.inline.buttons import (
    back_button,
    yes_button,
    cancel_button,
)


def back_yes_cancel_keyboard(l10n: FluentLocalization) -> InlineKeyboardMarkup:
    """
    The "Back", "Yes" and "Cancel" keyboard are formed.
    :param l10n: Language set by the user.
    :return: The "Back", "Yes" and "Cancel" keyboard.
    """

    back_yes_cancel_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                back_button(l10n),
                yes_button(l10n),
                cancel_button(l10n),
            ],
        ],
    )
    return back_yes_cancel_markup
