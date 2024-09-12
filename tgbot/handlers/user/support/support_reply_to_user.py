from aiogram import Router, Bot, F
from aiogram.exceptions import AiogramError
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.keyboards.inline import cancel_keyboard, reply_keyboard
from tgbot.services import get_user_localization, ClearKeyboard, create_user_link
from tgbot.states import Support

support_reply_to_user_router = Router()


@support_reply_to_user_router.callback_query(F.data.startswith("reply_to"))
async def support_reply_to_user(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
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
    storage: RedisStorage,
    bot: Bot,
):
    await ClearKeyboard.clear(message, storage)

    from_chat_id = message.chat.id
    message_id = message.message_id

    data = await state.get_data()
    id_user_recipient = data["id_user_recipient"]
    l10n_recipient = await get_user_localization(id_user_recipient)

    response = await api.users.get_user_by_id(id_user_recipient)
    user = response.get_model()
    full_name = user.full_name
    username = user.username
    user_link = await create_user_link(full_name, username)

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
