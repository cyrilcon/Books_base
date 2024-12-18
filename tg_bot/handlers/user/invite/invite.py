from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, LinkPreviewOptions
from aiogram.utils.deep_linking import create_start_link
from fluent.runtime import FluentLocalization

from config import config
from tg_bot.keyboards.inline import copy_invite_link_keyboard

common_invite_router = Router()


@common_invite_router.message(
    Command("invite"),
    flags={"safe_message": False},
)
async def invite(
    message: Message,
    l10n: FluentLocalization,
    bot: Bot,
):
    invite_link = await create_start_link(bot, str(message.from_user.id))
    price_discount_100 = config.price.discount.discount_100

    await message.answer(
        l10n.format_value(
            "invite",
            {"invite_link": invite_link, "price_discount_100": price_discount_100},
        ),
        link_preview_options=LinkPreviewOptions(prefer_small_media=True),
        reply_markup=copy_invite_link_keyboard(l10n, invite_link=invite_link),
    )
