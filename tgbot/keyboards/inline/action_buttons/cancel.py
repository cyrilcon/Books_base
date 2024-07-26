from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def cancel_keyboard(l10n) -> InlineKeyboardMarkup:
    """
    The "Cancel" button is formed.
    :param l10n: Language set by the user.
    :return: The "Cancel" button.
    """

    cancel_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=l10n.format_value("btn-cancel"), callback_data="cancel"
                )
            ]
        ],
    )
    return cancel_button
