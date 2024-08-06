from aiogram.types import InlineKeyboardMarkup

from tgbot.keyboards.inline.buttons import post_button, cancel_button


def post_cancel_keyboard(l10n) -> InlineKeyboardMarkup:
    """
    The "Post" and "Cancel" keyboard is formed.
    :param l10n: Language set by the user.
    :return: The "Post" and "Cancel" keyboard.
    """

    post_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                post_button(l10n),
                cancel_button(l10n),
            ],
        ],
    )
    return post_markup
