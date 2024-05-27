from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def support_answer_keyboard(l10n, id_user: int = None):
    """
    Формируется кнопка "Ответить" для сообщения с ошибкой, отправленная админам в чат тех-поддержки.
    :param l10n: Язык установленный у пользователя.
    :param id_user: ID пользователя.
    :return: Кнопка "Ответить".
    """

    if id_user is None:
        support_answer_button = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=l10n.format_value("button-support-reply"),
                        callback_data="support_reply_to_admin",
                    )
                ]
            ]
        )
    else:
        support_answer_button = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=l10n.format_value("button-support-reply"),
                        callback_data=f"support_answer:{id_user}",
                    )
                ]
            ],
        )
    return support_answer_button
