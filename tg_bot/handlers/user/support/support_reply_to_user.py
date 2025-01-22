from aiogram import Router, Bot, F
from aiogram.exceptions import AiogramError
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from tg_bot.api_client import api
from tg_bot.keyboards.inline import cancel_keyboard, reply_keyboard
from tg_bot.services import ClearKeyboard, create_user_link
from tg_bot.services.localization import get_fluent_localization
from tg_bot.states import Support

support_reply_to_user_router = Router()


@support_reply_to_user_router.callback_query(
    F.data.startswith("reply_to"),
    flags={
        "clear_keyboard": False,
        "safe_message": False,
    },
)
async def support_reply_to_user(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(call, storage)

    id_user = call.data.split(":")[-1]
    await state.update_data(id_user_recipient=id_user)

    sent_message = await call.message.answer(
        l10n.format_value("support-admin-reply-prompt"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(Support.reply_to_user)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=call.from_user.id,
        sent_message_id=sent_message.message_id,
    )
    await call.answer()


@support_reply_to_user_router.message(StateFilter(Support.reply_to_user))
async def support_reply_to_user_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    bot: Bot,
):
    from_chat_id = message.chat.id
    message_id = message.message_id

    data = await state.get_data()
    id_user_recipient = data["id_user_recipient"]

    response = await api.users.get_user_by_id(id_user=id_user_recipient)
    user = response.get_model()

    user_link = create_user_link(user.full_name, user.username)

    l10n_recipient = get_fluent_localization(user.language_code)
    try:
        sent_message = await bot.copy_message(
            chat_id=id_user_recipient,
            from_chat_id=from_chat_id,
            message_id=message_id,
        )
        await bot.send_message(
            chat_id=id_user_recipient,
            text=l10n_recipient.format_value("support-message-from-admin"),
            reply_markup=reply_keyboard(l10n),
            reply_to_message_id=sent_message.message_id,
        )
    except AiogramError:
        await message.answer(l10n.format_value("error-user-blocked-bot"))
    else:
        await message.answer(
            l10n.format_value(
                "support-admin-message-sent",
                {
                    "user_link": user_link,
                    "id_user": str(id_user_recipient),
                },
            )
        )
    await state.clear()
