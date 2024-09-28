from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.keyboards.inline import cancel_keyboard, edit_book_keyboard
from tg_bot.services import ClearKeyboard, generate_book_caption
from tg_bot.states import EditBook

edit_cover_router = Router()


@edit_cover_router.callback_query(F.data.startswith("edit_cover"))
async def edit_cover(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(call, storage)

    id_user = call.from_user.id

    id_book = int(call.data.split(":")[-1])
    response = await api.books.get_book_by_id(id_book=id_book)
    book = response.get_model()

    sent_message = await call.message.answer_photo(
        photo=book.cover,
        caption=l10n.format_value("edit-book-prompt-cover"),
        reply_markup=cancel_keyboard(l10n),
        show_caption_above_media=True,
    )
    await state.update_data(id_book_edited=id_book)
    await state.set_state(EditBook.edit_cover)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=id_user,
        sent_message_id=sent_message.message_id,
    )
    await call.answer()


@edit_cover_router.message(StateFilter(EditBook.edit_cover), F.photo)
async def edit_cover_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    cover = message.photo[-1].file_id

    data = await state.get_data()
    id_book_edited = data.get("id_book_edited")

    response = await api.books.update_book(id_book_edited, cover=cover)
    book = response.get_model()

    caption = await generate_book_caption(book_data=book, l10n=l10n)

    await message.answer(l10n.format_value("edit-book-success"))
    await message.answer_photo(
        photo=book.cover,
        caption=caption,
        reply_markup=edit_book_keyboard(l10n, book.id_book),
    )
    await state.clear()
