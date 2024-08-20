from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import (
    back_cancel_keyboard,
    cancel_keyboard,
    done_clear_back_cancel_keyboard,
)
from tgbot.services import ClearKeyboard
from tgbot.states import SendFiles

send_files_router_2 = Router()
send_files_router_2.message.filter(AdminFilter())


@send_files_router_2.callback_query(
    StateFilter(SendFiles.upload_files), F.data == "back"
)
async def back_to_send_files_1(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("send-files-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(SendFiles.select_user)


@send_files_router_2.message(StateFilter(SendFiles.upload_files), F.document)
async def send_files_2(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("send-files-upload-files-more"),
        reply_markup=done_clear_back_cancel_keyboard(l10n),
    )
    data = await state.get_data()
    files = data.get("files")
    file = message.document.file_id
    files.append(file)
    await state.update_data(files=files)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@send_files_router_2.callback_query(
    StateFilter(SendFiles.upload_files), F.data == "done"
)
async def done_send_files_2(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("send-files-write-caption"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.set_state(SendFiles.write_caption)


@send_files_router_2.callback_query(
    StateFilter(SendFiles.upload_files), F.data == "clear"
)
async def clear_send_files_2(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("send-files-upload-files-clear"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    files = []
    await state.update_data(files=files)
