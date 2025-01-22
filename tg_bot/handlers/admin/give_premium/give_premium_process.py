from aiogram import Router, F, Bot
from aiogram.exceptions import AiogramError
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from config import config
from tg_bot.api_client import api
from tg_bot.enums import MessageEffects
from tg_bot.keyboards.inline import cancel_keyboard, channel_keyboard
from tg_bot.services.localization import get_fluent_localization
from tg_bot.services.users import create_user_link, find_user
from tg_bot.states import GivePremium

give_premium_process_router = Router()


@give_premium_process_router.message(
    StateFilter(GivePremium.select_user),
    F.text,
)
async def give_premium_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    bot: Bot,
):
    user, response_message = await find_user(l10n, message.text)

    if not user:
        await message.answer(response_message, reply_markup=cancel_keyboard(l10n))
        return

    id_user = user.id_user
    user_link = create_user_link(user.full_name, user.username)

    if user.is_premium:
        await message.answer(
            l10n.format_value(
                "give-premium-error-user-already-has-premium",
                {"user_link": user_link, "id_user": str(id_user)},
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    l10n_recipient = get_fluent_localization(user.language_code)
    try:
        await bot.send_message(
            chat_id=id_user,
            text=l10n_recipient.format_value(
                "give-premium-success-message-for-user",
                {"channel_link": config.channel.link},
            ),
            message_effect_id=MessageEffects.CONFETTI,
            reply_markup=channel_keyboard(l10n),
        )
    except AiogramError:
        await message.answer(l10n.format_value("error-user-blocked-bot"))
    else:
        await api.users.premium.create_premium(id_user=id_user)

        if user.has_discount:
            await api.users.discounts.delete_discount(id_user=id_user)

        l10n_params = {
            "msg_id": "give-premium-success",
            "args": {"user_link": user_link, "id_user": str(id_user)},
        }

        await message.answer(
            text=l10n.format_value(
                msg_id=l10n_params["msg_id"],
                args=l10n_params["args"],
            )
        )

        l10n_chat = get_fluent_localization(config.chat.language_code)
        await bot.send_message(
            chat_id=config.chat.payment,
            text=l10n_chat.format_value(
                msg_id=l10n_params["msg_id"],
                args=l10n_params["args"],
            ),
        )
    await state.clear()
