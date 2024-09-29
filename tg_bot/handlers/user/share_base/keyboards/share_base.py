from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.keyboards.inline.buttons import (
    share_base_back_button,
    share_base_cancel_button,
)


def share_base_keyboard(l10n, base: int) -> InlineKeyboardMarkup:
    """
    The "share_base" keyboard is formed.
    :param l10n: Language set by the user.
    :param base: The number of bases the user has.
    :return: The "share_base" keyboard.
    """

    base_amounts = [10, 20, 30, 50, 100]
    buttons = []

    for amount in base_amounts:
        status_icon = "💎" if base >= amount else "❌"
        buttons.append(
            InlineKeyboardButton(
                text=f"{amount} {status_icon}",
                callback_data=f"share_base:{amount}",
            )
        )

    keyboard_buttons = [
        buttons[:3],
        buttons[3:],
        [share_base_back_button(l10n), share_base_cancel_button(l10n)],
    ]
    share_base_markup = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    return share_base_markup
