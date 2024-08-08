from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from infrastructure.books_base_api import api
from tgbot.keyboards.inline import cancel_keyboard, reply_keyboard
from tgbot.services import (
    get_user_language,
    ClearKeyboard,
    create_user_link,
    Messenger,
    Broadcaster,
)
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

    await call.answer(cache_time=1)
    sent_message = await call.message.answer(
        l10n.format_value("support-reply-to-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(Support.reply_to_user)

    await ClearKeyboard.safe_message(
        storage=storage,
        user_id=call.from_user.id,
        sent_message_id=sent_message.message_id,
    )


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
    l10n_recipient = await get_user_language(id_user_recipient)

    response = await api.users.get_user_by_id(id_user_recipient)
    user = response.result
    fullname = user["fullname"]
    username = user["username"]
    user_link = await create_user_link(fullname, username)

    is_sent = await Broadcaster.send_message(
        bot=bot,
        chat_id=id_user_recipient,
        from_chat_id=from_chat_id,
        message_id=message_id,
    )

    if is_sent:
        await Messenger.safe_send_message(
            bot=bot,
            user_id=id_user_recipient,
            text=l10n_recipient.format_value("support-from-admin"),
            reply_markup=reply_keyboard(l10n),
        )
        await message.answer(
            l10n.format_value(
                "support-success-for-admin",
                {
                    "user_link": user_link,
                    "id_user": str(id_user_recipient),
                },
            )
        )
    else:
        await message.answer(l10n.format_value("user-blocked-bot"))

    await state.clear()
