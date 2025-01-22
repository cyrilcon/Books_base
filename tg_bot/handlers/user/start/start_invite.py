import re
from datetime import datetime, timezone

from aiogram import Router, F, Bot
from aiogram.exceptions import AiogramError
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, LinkPreviewOptions
from fluent.runtime import FluentLocalization

from api.api_v1.schemas import UserSchema
from config import config
from tg_bot.api_client import api
from tg_bot.enums import MessageEffects
from tg_bot.keyboards.inline import channel_keyboard
from tg_bot.services import create_user_link
from tg_bot.services.bot import set_user_commands
from tg_bot.services.localization import get_fluent_localization

start_invite_router = Router()


@start_invite_router.message(
    CommandStart(deep_link=True, magic=F.args.regexp(re.compile(r"^\d+$"))),
    flags={"safe_message": False},
)
async def start_invite(
    message: Message,
    l10n: FluentLocalization,
    command: CommandObject,
    bot: Bot,
    user: UserSchema,
):
    referrer_id = int(command.args)
    referee_id = message.from_user.id

    # If the user who clicked the link is a bot, blacklist both the referrer and the user
    if message.from_user.is_bot:
        await api.users.blacklist.create_blacklist(id_user=referrer_id)
        await api.users.blacklist.create_blacklist(id_user=referee_id)
        return

    # If the user clicked on their own referral link
    if referrer_id == message.from_user.id:
        await message.answer(l10n.format_value("invite-error-self"))
        return

    await message.answer(
        l10n.format_value(
            "start",
            {
                "full_name": user.full_name,
                "channel_link": config.channel.link,
            },
        ),
        reply_markup=channel_keyboard(l10n),
    )
    await set_user_commands(
        bot=bot,
        id_user=user.id_user,
        is_admin=True if user.is_admin else False,
    )

    # Check if the user already has a referrer_id
    if user.referrer_id:
        return

    # Check if the user registered within the last 10 seconds
    registration_timedelta = datetime.now(timezone.utc) - user.registration_datetime
    if registration_timedelta.total_seconds() > 10:
        return

    # Verify if the referrer exists
    response = await api.users.get_user_by_id(id_user=referrer_id)
    if response.status != 200:
        return

    referrer = response.get_model()

    # If the referrer is a premium user or is blacklisted
    if referrer.is_premium or referrer.is_blacklisted:
        return

    price_discount_100 = config.price.discount.discount_100
    base_balance = referrer.base_balance + price_discount_100

    await api.users.update_user(id_user=referee_id, referrer_id=referrer_id)
    await api.users.update_user(
        id_user=referrer_id,
        base_balance=base_balance,
    )

    l10n_referrer = get_fluent_localization(referrer.language_code)

    user_link_referee = create_user_link(
        full_name=user.full_name,
        username=user.username,
    )

    try:
        await bot.send_message(
            chat_id=referrer_id,
            text=l10n_referrer.format_value(
                "invite-success",
                {
                    "user_link_referee": user_link_referee,
                    "price_discount_100": price_discount_100,
                    "base_balance": base_balance,
                },
            ),
            link_preview_options=LinkPreviewOptions(is_disabled=True),
            message_effect_id=MessageEffects.CONFETTI,
        )
    except AiogramError:
        pass

    user_link_referrer = create_user_link(
        full_name=referrer.full_name,
        username=referrer.username,
    )

    l10n_chat = get_fluent_localization(config.chat.language_code)
    await bot.send_message(
        chat_id=config.chat.payment,
        text=l10n_chat.format_value(
            "invite-success-message-for-admin",
            {
                "user_link_referrer": user_link_referrer,
                "referrer_id": str(referrer_id),
                "user_link_referee": user_link_referee,
                "referee_id": str(referee_id),
                "base_balance": base_balance,
            },
        ),
    )
