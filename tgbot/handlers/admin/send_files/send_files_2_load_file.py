from aiogram import Router, F, Bot
from aiogram.exceptions import AiogramError
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.config import Config
from tgbot.filters import AdminFilter
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import (
    back_and_cancel_keyboard,
    cancel_keyboard,
    done_clear_back_cancel_keyboard,
)
from tgbot.services import get_user_language, safe_send_message
from tgbot.states import SendFiles

send_files_router_2 = Router()
send_files_router_2.message.filter(AdminFilter())


@send_files_router_2.callback_query(StateFilter(SendFiles.load_files), F.data == "back")
async def back_to_send_files_1(call: CallbackQuery, state: FSMContext):
    """
    Возвращение назад к выбору пользователя.
    :param call: Нажатая кнопка "« Назад".
    :param state: FSM (SendFiles).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("send-files-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(SendFiles.select_recipient)


@send_files_router_2.message(StateFilter(SendFiles.load_files), F.document)
async def send_files_2(message: Message, bot: Bot, state: FSMContext):
    """
    Загрузка файлов.
    :param message: Сообщение с ожидаемым(и) файлами.
    :param bot: Экземпляр бота.
    :param state: FSM (SendFiles).
    :return: Файл для отправки пользователю.
    """

    await delete_keyboard(bot, message)

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    data = await state.get_data()
    files = data.get("files")

    file = message.document.file_id
    files.append(file)
    await state.update_data(files=files)

    await message.answer(
        l10n.format_value("send-files-more"),
        reply_markup=done_clear_back_cancel_keyboard(l10n),
    )


@send_files_router_2.callback_query(StateFilter(SendFiles.load_files), F.data == "done")
async def done_send_files_2(
    call: CallbackQuery, state: FSMContext, bot: Bot, config: Config
):
    """
    Отправка файлов пользователю.
    :param call: Нажатая кнопка "Готово".
    :param state: FSM (SendFiles).
    :param bot: Экземпляр бота.
    :param config: Config с параметрами бота.
    :return: Отправка файлов пользователю.
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    data = await state.get_data()
    files = data.get("files")
    id_user_recipient = data.get("id_user_recipient")
    l10n_recipient = await get_user_language(id_user_recipient)

    is_sent = await safe_send_message(
        config=config,
        bot=bot,
        id_user=id_user_recipient,
        text=l10n_recipient.format_value("send-files-received"),
    )

    if is_sent:
        for file in files:
            try:
                await bot.send_document(chat_id=id_user_recipient, document=file)
            except AiogramError:
                await call.message.answer(
                    l10n.format_value("send-files-user-did-not-receive-file")
                )
        await call.message.edit_text(l10n.format_value("send-files-done"))
    else:
        await call.message.edit_text(l10n.format_value("user-blocked-bot"))

    await call.answer(cache_time=1)
    await state.clear()


@send_files_router_2.callback_query(
    StateFilter(SendFiles.load_files), F.data == "clear"
)
async def clear_send_files_2(call: CallbackQuery, state: FSMContext):
    """
    Очистка списка всех файлов.
    :param call: Нажатая кнопка "Стереть".
    :param state: FSM (SendFiles).
    :return: Сообщение для добавления файлов сначала
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("send-files-clear"),
        reply_markup=back_and_cancel_keyboard(l10n),
    )
    files = []
    await state.update_data(files=files)
