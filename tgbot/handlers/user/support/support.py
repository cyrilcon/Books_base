from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tgbot.config import config
from tgbot.keyboards.inline import cancel_keyboard, reply_keyboard
from tgbot.services import ClearKeyboard, create_user_link, Messenger
from tgbot.states import Support

support_router = Router()


@support_router.message(Command("support"))
async def support(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("support"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(Support.reply_to_admin)

    await ClearKeyboard.safe_message(
        storage=storage,
        user_id=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@support_router.message(StateFilter(Support.reply_to_admin))
async def support_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    await ClearKeyboard.clear(message, storage)

    id_user = message.from_user.id
    fullname = message.from_user.full_name
    username = message.from_user.username
    user_link = await create_user_link(fullname, username)

    await bot.forward_message(
        chat_id=config.tg_bot.support_chat,
        from_chat_id=message.chat.id,
        message_id=message.message_id,
    )
    await Messenger.safe_send_message(
        bot=bot,
        user_id=config.tg_bot.support_chat,
        text=l10n.format_value(
            "support-from-user",
            {
                "user_link": user_link,
                "id_user": str(id_user),
            },
        ),
        reply_markup=reply_keyboard(l10n, id_user=id_user),
    )

    data = await state.get_data()
    from_button = data["from_button"]

    if from_button:
        await message.answer(l10n.format_value("support-success-for-user"))
    else:
        await message.answer(l10n.format_value("support-success"))
    await state.clear()
