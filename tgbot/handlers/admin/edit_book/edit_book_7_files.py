from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram.utils.media_group import MediaGroupBuilder
from fluent.runtime import FluentLocalization

from infrastructure.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import (
    cancel_keyboard,
    edit_book_keyboard,
    done_clear_cancel_keyboard,
)
from tgbot.services import (
    ClearKeyboard,
    formats_to_list,
    generate_book_caption,
    Messenger,
)
from tgbot.states import EditBook

edit_book_router_7 = Router()
edit_book_router_7.message.filter(AdminFilter())


@edit_book_router_7.callback_query(F.data.startswith("edit_files"))
async def edit_files(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await call.answer(cache_time=1)

    id_book = int(call.data.split(":")[-1])
    response = await api.books.get_book_by_id(id_book)
    book = response.result

    album_builder = MediaGroupBuilder()
    for file in book["files"]:
        album_builder.add_document(media=file["file"])
    await call.message.answer_media_group(media=album_builder.build())

    sent_message = await call.message.answer(
        l10n.format_value("edit-book-files"),
        reply_markup=cancel_keyboard(l10n),
    )

    await state.update_data(id_book_edited=id_book)
    await state.set_state(EditBook.edit_files)

    await ClearKeyboard.safe_message(
        storage=storage,
        user_id=call.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@edit_book_router_7.message(StateFilter(EditBook.edit_files), F.document)
async def edit_files_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    data = await state.get_data()
    files = data.get("files")
    files, text = await formats_to_list(message, l10n, files)

    await state.update_data(files=files)
    sent_message = await message.answer(
        text,  # TODO: add delete button (future feature)
        reply_markup=done_clear_cancel_keyboard(l10n),
    )

    await ClearKeyboard.safe_message(
        storage=storage,
        user_id=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@edit_book_router_7.callback_query(StateFilter(EditBook.edit_files), F.data == "done")
async def done_edit_files(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    await call.answer(cache_time=1)

    data = await state.get_data()
    id_book_edited = data.get("id_book_edited")
    files = data.get("files")

    response = await api.books.update_book(id_book_edited, files=files)
    book = response.result

    caption = await generate_book_caption(data=book, l10n=l10n)
    caption_length = len(caption)

    if caption_length <= 1024:
        await call.message.edit_text(
            l10n.format_value("edit-book-success"), reply_markup=None
        )
        await Messenger.safe_send_message(
            bot=bot,
            user_id=call.from_user.id,
            text=caption,
            photo=book["cover"],
            reply_markup=edit_book_keyboard(l10n, book["id_book"]),
        )
        await state.clear()
    else:
        sent_message = await call.message.answer(
            l10n.format_value(
                "edit-book-caption-too-long",
                {"caption_length": caption_length},
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            user_id=call.from_user.id,
            sent_message_id=sent_message.message_id,
        )


@edit_book_router_7.callback_query(StateFilter(EditBook.edit_files), F.data == "clear")
async def clear_edit_files(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("edit-book-files"),
        reply_markup=cancel_keyboard(l10n),
    )
    files = []
    await state.update_data(files=files)
