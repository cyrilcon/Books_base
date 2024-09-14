from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from fluent.runtime import FluentLocalization

from tgbot.keyboards.inline.buttons import news_channel_button


def view_news_keyboard(
    l10n: FluentLocalization,
    orders_count: int,
    position: int = 1,
    language_code: str = "ru",
) -> InlineKeyboardMarkup:
    """
    A keyboard with pagination for viewing orders is formed.
    :param l10n: Language set by the user.
    :param orders_count: Number of all articles.
    :param position: Article position in the database.
    :param language_code: IETF language tag of the user's language.
    :return: Keyboard with pagination for viewing articles.
    """

    action_buttons = []

    if orders_count > 1:
        if position > 1:
            action_buttons.append(
                InlineKeyboardButton(
                    text=f"⬅️", callback_data=f"article_position:{position - 1}"
                )
            )

        action_buttons.append(
            InlineKeyboardButton(
                text=f"{l10n.format_value("page")} {position}/{orders_count}",
                callback_data=f"pagination_info",
            )
        )

        if position < orders_count:
            action_buttons.append(
                InlineKeyboardButton(
                    text=f"➡️", callback_data=f"article_position:{position + 1}"
                )
            )

    view_news_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            action_buttons,
            [
                news_channel_button(l10n, language_code=language_code),
            ],
        ]
    )

    return view_news_markup
