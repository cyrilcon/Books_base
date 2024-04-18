from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.filters import AdminFilter
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import (
    back_and_cancel_buttons,
    ready_clear_back_cancel_buttons,
)
from tgbot.services import get_user_language
from tgbot.states import AddBook

add_book_router_7 = Router()
add_book_router_7.message.filter(AdminFilter())


@add_book_router_7.callback_query(StateFilter(AddBook.add_files), F.data == "back")
async def back_to_add_book_6(call: CallbackQuery, state: FSMContext):
    """
    Возвращение назад к добавлению обложки.
    :param call: Нажатая кнопка "« Назад".
    :param state: FSM (AddBook).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("add-book-cover"),
        reply_markup=back_and_cancel_buttons,
    )
    await state.set_state(AddBook.add_cover)


@add_book_router_7.message(StateFilter(AddBook.add_files), F.document)
async def add_book_7(message: Message, bot: Bot, state: FSMContext):
    """
    Добавление файлов.
    :param message: Сообщение с ожидаемыми файлами.
    :param bot: Экземпляр бота.
    :param state: FSM (AddBook).
    :return: Сообщение для выбора цены и переход в FSM (select_price).
    """

    await delete_keyboard(bot, message)

    data = await state.get_data()
    files = data.get("files")
    files, text = await add_formats_to_dict(files, message)

    await state.update_data(files=files)
    await message.answer(text, reply_markup=ready_clear_back_cancel_buttons)


@add_book_router_7.callback_query(StateFilter(AddBook.add_files), F.data == "done")
async def done_add_book_7(call: CallbackQuery, state: FSMContext):
    """
    Выбор цены.
    :param call: Нажатая кнопка "Готово".
    :param state: FSM (AddBook).
    :return: Сообщение для выбора цены и переход в FSM (select_price).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.message.edit_text(
        l10n.format_value("add-book-price"),
        reply_markup=back_and_cancel_buttons,
    )
    await state.set_state(AddBook.select_price)


@add_book_router_7.callback_query(StateFilter(AddBook.add_files), F.data == "clear")
async def clear_add_book_7(call: CallbackQuery, state: FSMContext):
    """
    Очистка списка всех файлов.
    :param call: Нажатая кнопка "Стереть".
    :param state: FSM (AddBook).
    :return: Сообщение для добавления файлов сначала
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.message.edit_text(
        l10n.format_value("add-book-files"),
        reply_markup=back_and_cancel_buttons,
    )
    files = {}
    await state.update_data(files=files)


async def add_formats_to_dict(files, message) -> (dict, str):
    """
    Добавляются файлы и их форматы в словарь.
    :param files: (Файл: формат) словарь.
    :param message: Ожидаемый файл с книгой.
    :return: Словарь с файлами и их форматами.
    """

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    file = message.document.file_id
    file_format = message.document.file_name.split(".")[-1]

    if files is None:
        files = {}

    if file_format not in files:
        files[file_format] = file
        selected_text = "add-book-files-send-more"
    else:
        selected_text = "add-book-files-already-sent"

    formats = ", ".join(f"{format}" for format in files)
    text = l10n.format_value(selected_text, {"formats": formats})

    return files, text
