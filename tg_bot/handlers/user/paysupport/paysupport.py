from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, LinkPreviewOptions
from fluent.runtime import FluentLocalization

command_paysupport_router = Router()


@command_paysupport_router.message(Command("paysupport"))
async def paysupport(
    message: Message,
    l10n: FluentLocalization,
):
    await message.answer(
        l10n.format_value("paysupport"),
        link_preview_options=LinkPreviewOptions(
            url=l10n.format_value("article-payment-and-refund-policy"),
            prefer_large_media=True,
        ),
    )
