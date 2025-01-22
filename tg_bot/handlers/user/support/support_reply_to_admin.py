from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery, Message
from fluent.runtime import FluentLocalization

from config import config
from tg_bot.keyboards.inline import cancel_keyboard, reply_keyboard
from tg_bot.services.messaging import ClearKeyboard
from tg_bot.services.users import create_user_link
from tg_bot.states import Support

support_reply_to_admin_router = Router()


@support_reply_to_admin_router.callback_query(
    F.data == "reply_to:admin",
    flags={
        "clear_keyboard": False,
        "safe_message": False,
    },
)
async def support_reply_to_admin(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(call, storage)

    sent_message = await call.message.answer(
        l10n.format_value("support-user-reply-prompt"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.update_data(reply_from_button=True)
    await state.set_state(Support.reply_to_admin)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=call.from_user.id,
        sent_message_id=sent_message.message_id,
    )
    await call.answer()


@support_reply_to_admin_router.message(StateFilter(Support.reply_to_admin))
async def support_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    bot: Bot,
):
    id_user = message.from_user.id
    user_link = create_user_link(
        full_name=message.from_user.full_name,
        username=message.from_user.username,
    )

    sent_message = await bot.forward_message(
        chat_id=config.chat.support,
        from_chat_id=message.chat.id,
        message_id=message.message_id,
    )
    await bot.send_message(
        chat_id=config.chat.support,
        text=l10n.format_value(
            "support-message-from-user",
            {
                "user_link": user_link,
                "id_user": str(id_user),
            },
        ),
        reply_markup=reply_keyboard(l10n, id_user=id_user),
        reply_to_message_id=sent_message.message_id,
    )

    data = await state.get_data()
    reply_from_button = data["reply_from_button"]

    if reply_from_button:
        await message.answer(l10n.format_value("support-user-message-sent"))
    else:
        await message.answer(l10n.format_value("support-user-success"))
    await state.clear()
