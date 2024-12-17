from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, LinkPreviewOptions
from aiogram.utils.deep_linking import create_start_link
from fluent.runtime import FluentLocalization

common_invite_router = Router()


@common_invite_router.message(Command("invite"))
async def invite(
    message: Message,
    l10n: FluentLocalization,
    bot: Bot,
):
    link = await create_start_link(bot, str(message.from_user.id))

    await message.answer(
        l10n.format_value("invite", {"link": link}),
        link_preview_options=LinkPreviewOptions(prefer_small_media=True),
    )
