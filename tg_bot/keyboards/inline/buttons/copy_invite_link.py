from aiogram.types import InlineKeyboardButton, CopyTextButton
from fluent.runtime import FluentLocalization


def copy_invite_link_button(
    l10n: FluentLocalization,
    invite_link: str,
) -> InlineKeyboardButton:
    """
    The "Share our store" button is formed.
    :param l10n: Language set by the user.
    :param invite_link: Invite link.
    :return: The "Share our store" button.
    """

    copy_invite_link = InlineKeyboardButton(
        text=l10n.format_value("button-copy-invite-link"),
        copy_text=CopyTextButton(text=invite_link),
    )
    return copy_invite_link
