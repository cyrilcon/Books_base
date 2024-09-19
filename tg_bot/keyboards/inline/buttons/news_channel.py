from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def news_channel_button(
    l10n: FluentLocalization,
    language_code: str = "ru",
) -> InlineKeyboardButton:
    """
    The "News channel" deep link button is formed.
    :param l10n: Language set by the user.
    :param language_code: IETF language tag of the user's language.
    :return: The "News channel" deep link button.
    """

    news_channel = InlineKeyboardButton(
        text=l10n.format_value("button-news-channel"),
        callback_data=f"news_channel",
        url=f"https://t.me/Books_base_news_{language_code}",
    )
    return news_channel
