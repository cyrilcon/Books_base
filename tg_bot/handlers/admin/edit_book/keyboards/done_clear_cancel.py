from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline.buttons import (
    done_button,
    clear_button,
    delete_button,
    cancel_button,
)


def done_clear_delete_cancel_keyboard(l10n: FluentLocalization) -> InlineKeyboardMarkup:
    """
    The "done_clear_delete_cancel" keyboard is formed.
    :param l10n: Language set by the user.
    :return: The "done_clear_delete_cancel" keyboard.
    """

    done_clear_delete_cancel_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                done_button(l10n),
                clear_button(l10n),
            ],
            [
                delete_button(l10n),
                cancel_button(l10n),
            ],
        ],
    )
    return done_clear_delete_cancel_markup
