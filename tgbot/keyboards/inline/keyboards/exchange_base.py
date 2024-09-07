from aiogram.types import InlineKeyboardMarkup

from tgbot.keyboards.inline.buttons import exchange_base_button


def exchange_base_keyboard(l10n) -> InlineKeyboardMarkup:
    """
    The "exchange_base" keyboard is formed.
    :param l10n: Language set by the user.
    :return: The "exchange_base" keyboard.
    """

    exchange_base_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                exchange_base_button(l10n),
            ]
        ],
    )
    return exchange_base_markup
