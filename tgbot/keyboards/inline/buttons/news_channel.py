from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def news_channel_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "News channel" deep link button is formed.
    :param l10n: Language set by the user.
    :return: The "News channel" deep link button.
    """

    news_channel = InlineKeyboardButton(
        text=l10n.format_value("button-news-channel"),
        callback_data=f"news_channel",
        url=f"https://t.me/Books_base",
    )
    return news_channel
