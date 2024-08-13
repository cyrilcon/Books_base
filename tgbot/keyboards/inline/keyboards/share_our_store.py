from aiogram.types import InlineKeyboardMarkup

from tgbot.keyboards.inline.buttons import share_our_store_button, cancel_button


def share_our_store_keyboard(l10n) -> InlineKeyboardMarkup:
    """
    The "Share our store" and "Cancel" keyboard is formed.
    :param l10n: Language set by the user.
    :return: The "Share our store" and "Cancel" keyboard.
    """

    share_our_store_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                share_our_store_button(l10n),
            ],
            [
                cancel_button(l10n),
            ],
        ],
    )
    return share_our_store_markup
