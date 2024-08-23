from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from tgbot.keyboards.inline.buttons import (
    done_button,
    clear_button,
    back_button,
    cancel_button,
)


def done_clear_back_cancel_keyboard(l10n: FluentLocalization) -> InlineKeyboardMarkup:
    """
    The "done_clear_back_cancel" keyboard is formed.
    :param l10n: Language set by the user.
    :return: The "done_clear_back_cancel" keyboard.
    """

    done_clear_back_cancel_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                done_button(l10n),
                clear_button(l10n),
            ],
            [
                back_button(l10n),
                cancel_button(l10n),
            ],
        ],
    )
    return done_clear_back_cancel_markup
