from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from infrastructure.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import cancel_keyboard, back_and_cancel_keyboard
from tgbot.services import get_user_language, check_username, get_url_user
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

    await state.set_state(SendFiles.select_user)

    files = []
    await state.update_data(files=files)


@send_files_router_1.message(StateFilter(SendFiles.select_user))
async def send_file_1_process(message: Message, bot: Bot, state: FSMContext):
    """
    Выбор пользователя для отправки файлов.
    :param message: Сообщение с ожидаемым именем пользователя или его ID.
    :param bot: Экземпляр бота.
    :param state: FSM (SendFiles).
    :return: Сообщение для загрузки файлов и переход в FSM (load_files).
    """

    await delete_keyboard(bot, message)

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    message_text = message.text

    if message_text.isdigit():
        id_user = int(message_text)

        response = await api.users.get_user(id_user)
        status = response.status

        if status == 200:
            await user_found(response, message, l10n, state)
        else:
            await message.answer(
                l10n.format_value("user-not-found-by-id", {"id_user": str(id_user)}),
                reply_markup=cancel_keyboard(l10n),
            )
    else:
        selected_user = check_username(message_text)

        if selected_user:
            response = await api.users.get_user_by_username(selected_user)
            status = response.status

            if status == 200:
                await user_found(response, message, l10n, state)
            else:
                await message.answer(
                    l10n.format_value(
                        "user-not-found-by-username", {"username": selected_user}
                    ),
                    reply_markup=cancel_keyboard(l10n),
                )
        else:
            await message.answer(
                l10n.format_value("username-incorrect"),
                reply_markup=cancel_keyboard(l10n),
            )


async def user_found(response, message, l10n, state):
    """
    Сценарий, если пользователь найден.
    :param response: Полученный ответ от api.
    :param message: Сообщение с ожидаемым именем пользователя или его ID.
    :param l10n: Язык установленный у пользователя.
    :param state: FSM (SendFiles).
    :return: Отправка сообщения для загрузки файлов и переход в FSM (load_files).
    """

    user = response.result
    id_user_recipient = user["id_user"]
    fullname = user["fullname"]
    username = user["username"]

    url_user = await get_url_user(fullname, username)

    await message.answer(
        l10n.format_value(
            "send-files-load-file",
            {"url_user": url_user, "id_user": str(id_user_recipient)},
        ),
        reply_markup=back_and_cancel_keyboard(l10n),
    )

    await state.update_data(id_user_recipient=id_user_recipient)
    await state.set_state(SendFiles.load_files)
