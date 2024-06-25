from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def share_our_store_keyboard(l10n) -> InlineKeyboardMarkup:
    """
    Формируется кнопка "Поделиться нашим магазином".
    :param l10n: Язык установленный у пользователя.
    :return: Кнопка "Поделиться нашим магазином".
    """

    share_our_store_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=l10n.format_value("button-share-our-store"),
                    switch_inline_query="– это крутой бот!! ...",  # TODO: добавить локализацию
                )
            ],
        ],
    )
    return share_our_store_button
