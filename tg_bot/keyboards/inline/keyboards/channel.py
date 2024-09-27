from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline.buttons import channel_button


def channel_keyboard(l10n: FluentLocalization) -> InlineKeyboardMarkup:
    """
    The "channel_keyboard" keyboard is formed.
    :param l10n: Language set by the user.
    :return: The "channel_keyboard" keyboard.
    """

    channel_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                channel_button(l10n),
            ]
        ],
    )
    return channel_markup
