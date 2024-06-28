from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import cancel_keyboard
from tgbot.services import get_user_language, select_user
from tgbot.states import SendFiles

send_files_router_1 = Router()
send_files_router_1.message.filter(AdminFilter())


@send_files_router_1.message(Command("send_files"))
async def send_file_1(message: Message, state: FSMContext):
    """
    Обработка команды /send_files.
    :param message: Команда /send_files.
    :param state: FSM (SendFiles).
    :return: Сообщение для отправки файлов пользователю и переход в FSM (SendFiles).
    """

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    await message.answer(
        l10n.format_value("send-files-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )

    await state.set_state(SendFiles.select_recipient)
    files = []
    await state.update_data(files=files)


@send_files_router_1.message(StateFilter(SendFiles.select_recipient))
async def send_file_1_process(message: Message, bot: Bot, state: FSMContext):
    """
    Выбор пользователя для отправки файлов.
    :param message: Сообщение с ожидаемым именем пользователя или его ID.
    :param bot: Экземпляр бота.
    :param state: FSM (SendFiles).
    :return: Сообщение для загрузки файлов и переход в FSM (load_files).
    """

    text = "send-files-load-file"
    await select_user(message, bot, state, SendFiles.load_files, text)
