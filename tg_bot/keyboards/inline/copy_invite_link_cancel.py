from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline.buttons import copy_invite_link_button, cancel_button


def copy_invite_link_cancel_keyboard(
    l10n: FluentLocalization,
    invite_link: str,
) -> InlineKeyboardMarkup:
    """
    The "share_our_store" keyboard is formed.
    :param l10n: Language set by the user.
    :param invite_link: Invite link.
    :return: The "share_our_store" keyboard.
    """

    copy_invite_link_cancel_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                copy_invite_link_button(l10n, invite_link=invite_link),
            ],
            [
                cancel_button(l10n),
            ],
        ],
    )
    return copy_invite_link_cancel_markup
