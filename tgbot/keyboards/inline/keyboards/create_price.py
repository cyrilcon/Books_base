from aiogram.types import InlineKeyboardMarkup

from tgbot.keyboards.inline.buttons import (
    create_price_85_button,
    create_price_50_button,
    not_post_button,
    not_from_user_button,
    back_button,
    cancel_button,
)


def create_price_keyboard(l10n) -> InlineKeyboardMarkup:
    """
    The "create_price" keyboard is formed.
    :param l10n: Language set by the user.
    :return: The "create_price" keyboard.
    """

    create_price_keyboard_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                create_price_85_button(l10n),
                create_price_50_button(l10n),
            ],
            [
                not_post_button(l10n),
                not_from_user_button(l10n),
            ],
            [
                back_button(l10n),
                cancel_button(l10n),
            ],
        ],
    )
    return create_price_keyboard_markup
