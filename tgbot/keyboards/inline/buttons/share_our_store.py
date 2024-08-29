from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def share_our_store_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Share our store" button is formed.
    :param l10n: Language set by the user.
    :return: The "Share our store" button.
    """

    share_our_store = InlineKeyboardButton(
        text=l10n.format_value("button-share-our-store"),
        switch_inline_query="– это крутой бот!! ...",  # TODO: Дописать!!
    )
    return share_our_store
