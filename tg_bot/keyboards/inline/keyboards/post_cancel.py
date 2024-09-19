from aiogram.types import InlineKeyboardMarkup

from tg_bot.keyboards.inline.buttons import post_button, cancel_button


def post_cancel_keyboard(l10n) -> InlineKeyboardMarkup:
    """
    The "post_cancel" keyboard is formed.
    :param l10n: Language set by the user.
    :return: The "post_cancel" keyboard.
    """

    post_cancel_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                post_button(l10n),
                cancel_button(l10n),
            ],
        ],
    )
    return post_cancel_markup
