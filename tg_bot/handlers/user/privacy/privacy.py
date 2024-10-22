from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, LinkPreviewOptions
from fluent.runtime import FluentLocalization

command_privacy_router = Router()


@command_privacy_router.message(Command("privacy"))
async def privacy(
    message: Message,
    l10n: FluentLocalization,
):
    await message.answer(
        l10n.format_value("privacy"),
        link_preview_options=LinkPreviewOptions(
            url=l10n.format_value("article-privacy-policy"),
            prefer_large_media=True,
        ),
    )
