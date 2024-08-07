from aiogram import Router, F, Bot
from aiogram.exceptions import AiogramError
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import (
    cancel_keyboard,
)
from tgbot.services import (
    Messenger,
    get_user_language,
    send_files_in_groups,
    ClearKeyboard,
)
from tgbot.states import SendFiles

send_files_router_3 = Router()
send_files_router_3.message.filter(AdminFilter())


@send_files_router_3.callback_query(
    StateFilter(SendFiles.write_caption), F.data == "back"
)
async def back_to_send_files_2(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("send-files-upload-files-clear"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(SendFiles.upload_files)
    files = []
    await state.update_data(files=files)


@send_files_router_3.message(StateFilter(SendFiles.write_caption), F.text)
async def send_files_3(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    await ClearKeyboard.clear(message, storage)

    data = await state.get_data()
    files = data.get("files")
    id_user_recipient = data.get("id_user_recipient")
    l10n_recipient = await get_user_language(id_user_recipient)

    is_sent = await Messenger.safe_send_message(
        bot=bot,
        user_id=id_user_recipient,
        text=l10n_recipient.format_value("send-files-from-admin"),
    )

    if is_sent:
        try:
            await send_files_in_groups(
                bot=bot, chat_id=id_user_recipient, files=files, text=message.text
            )
            await message.answer(l10n.format_value("send-files-success"))
        except AiogramError:
            await message.answer(l10n.format_value("send-files-error"))
    else:
        await message.answer(l10n.format_value("user-blocked-bot"))

    await state.clear()


@send_files_router_3.callback_query(
    StateFilter(SendFiles.upload_files), F.data == "done"
)
async def done_send_files_3(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    bot: Bot,
):
    data = await state.get_data()
    files = data.get("files")
    id_user_recipient = data.get("id_user_recipient")
    l10n_recipient = await get_user_language(id_user_recipient)

    is_sent = await Messenger.safe_send_message(
        bot=bot,
        user_id=id_user_recipient,
        text=l10n_recipient.format_value("send-files-from-admin"),
    )

    if is_sent:
        try:
            await send_files_in_groups(bot=bot, chat_id=id_user_recipient, files=files)
            await call.message.edit_text(l10n.format_value("send-files-success"))
        except AiogramError:
            await call.message.edit_text(l10n.format_value("send-files-error"))
    else:
        await call.message.edit_text(l10n.format_value("user-blocked-bot"))

    await call.answer(cache_time=1)
    await state.clear()
