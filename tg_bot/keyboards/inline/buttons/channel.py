from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization

from tg_bot.config import config


def channel_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Channel" button is formed.
    :param l10n: Language set by the user.
    :return: The "Channel" button.
    """

    channel = InlineKeyboardButton(
        text=l10n.format_value("button-all-books"),
        url=config.channel.main_link,
    )
    return channel
