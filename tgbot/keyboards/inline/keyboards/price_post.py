from aiogram.types import InlineKeyboardMarkup

from tgbot.keyboards.inline.buttons import (
    price_85_button,
    price_50_button,
    do_not_publish_button,
    not_from_user_button,
    back_button,
    cancel_button,
)


def price_post_keyboard(l10n) -> InlineKeyboardMarkup:
    """
    The "85₽", "50₽", "Don't publish", "Not from user", "Back" and "Cancel" keyboard are formed.
    :param l10n: Language set by the user.
    :return: The "85₽", "50₽", "Don't publish", "Not from user", "Back" and "Cancel" keyboard.
    """

    price_post_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                price_85_button(l10n),
                price_50_button(l10n),
            ],
            [
                do_not_publish_button(l10n),
                not_from_user_button(l10n),
            ],
            [
                back_button(l10n),
                cancel_button(l10n),
            ],
        ],
    )
    return price_post_markup
