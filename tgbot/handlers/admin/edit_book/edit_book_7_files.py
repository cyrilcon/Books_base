from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram.utils.media_group import MediaGroupBuilder

from infrastructure.books_base_api import api
from tgbot.config import Config
from tgbot.filters import AdminFilter
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import (
    cancel_keyboard,
    done_cancel_keyboard,
    edit_keyboard,
)
from tgbot.services import get_user_language, forming_text, safe_send_message
from tgbot.states import EditBook

edit_book_router_7 = Router()
edit_book_router_7.message.filter(AdminFilter())


@edit_book_router_7.callback_query(F.data.startswith("edit_files"))
async def edit_files(call: CallbackQuery, state: FSMContext):
    """
    Обработка кнопки "Файлы".
    :param call: Кнопка "Файлы".
    :param state: FSM (EditBook).
    :return: Сообщение для изменения файлов книги и переход в FSM (edit_files).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.answer(cache_time=1)

    id_book = int(call.data.split(":")[-1])
    response = await api.books.get_book(id_book)
    book = response.result

    album_builder = MediaGroupBuilder(
        # caption="Общая подпись для альбома"
    )

    for file in book["files"]:
        album_builder.add_document(media=file["file"])

    await call.message.answer_media_group(media=album_builder.build())

    await call.message.answer(
        l10n.format_value(
            "edit-book-files",
            {"files": f"<code>{book["description"]}</code>"},
        ),
        reply_markup=cancel_keyboard(l10n),
    )

    await state.update_data(id_edit_book=id_book)
    await state.set_state(EditBook.edit_files)


@edit_book_router_7.message(StateFilter(EditBook.edit_files), F.document)
async def edit_files_file_sent(message: Message, bot: Bot, state: FSMContext):
    """
    Добавление файлов.
    :param message: Сообщение с ожидаемыми файлами.
    :param bot: Экземпляр бота.
    :param state: FSM (EditBook).
    :return: Сообщение для изменения файлов книги.
    """

    await delete_keyboard(bot, message)

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    data = await state.get_data()
    files = data.get("files")
    files, text = await add_formats_to_dict(files, message)

    await state.update_data(files=files)
    await message.answer(text, reply_markup=done_cancel_keyboard(l10n))


@edit_book_router_7.callback_query(StateFilter(EditBook.edit_files), F.data == "done")
async def done_edit_files(
    call: CallbackQuery, bot: Bot, state: FSMContext, config: Config
):
    """
    Изменение файлов книги.
    :param call: Нажатая кнопка "Готово".
    :param bot: Экземпляр бота.
    :param state: FSM (EditBook).
    :param config: Config с параметрами бота.
    :return: Сообщение об успешном изменении файлов.
    """

    await call.answer(cache_time=1)

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    data = await state.get_data()
    id_edit_book = data.get("id_edit_book")
    files = data.get("files")

    response = await api.books.update_book(id_edit_book, files=files)
    status = response.status
    book = response.result

    if status == 200:
        post_text = await forming_text(book, l10n)

        await call.message.edit_text(
            l10n.format_value("edit-book-successfully-changed"), reply_markup=None
        )
        await safe_send_message(
            config=config,
            bot=bot,
            id_user=id_user,
            text=post_text,
            photo=book["cover"],
            reply_markup=edit_keyboard(l10n, book["id_book"]),
        )
        await state.clear()


async def add_formats_to_dict(files, message) -> (list, str):
    """
    Добавляются файлы и их форматы в список.
    :param files: Список словарей с файлами и их форматами.
    :param message: Ожидаемый файл с книгой.
    :return: Список с файлами и их форматами.
    """

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    file = message.document.file_id
    file_format = message.document.file_name.split(".")[-1]

    if files is None:
        files = []

    # Проверка на существование формата в списке и обновление файла
    for file_dict in files:
        if file_dict["format"] == file_format:
            file_dict["file"] = file
            break
    else:
        file_dict = {"format": file_format, "file": file}
        files.append(file_dict)

    formats = ", ".join(f"{file['format']}" for file in files)
    text = l10n.format_value("edit-book-files-send-more", {"formats": formats})

    return files, text
