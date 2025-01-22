from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.api_client import api
from tg_bot.keyboards.inline import cancel_keyboard, edit_book_keyboard
from tg_bot.services import generate_book_caption, ClearKeyboard
from tg_bot.services.utils import is_valid_book_article
from tg_bot.states import EditBook

edit_book_process_router = Router()


@edit_book_process_router.message(
    StateFilter(EditBook.select_book),
    F.text,
    flags={"safe_message": False},
)
async def edit_book_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    article = message.text

    if not is_valid_book_article(article):
        sent_message = await message.answer(
            l10n.format_value("edit-book-error-invalid-article"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    id_book = int(article.lstrip("#"))

    response = await api.books.get_book_by_id(id_book=id_book)

    if response.status != 200:
        sent_message = await message.answer(
            l10n.format_value("edit-book-error-article-not-found"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    book = response.get_model()
    caption = await generate_book_caption(book_data=book, l10n=l10n)

    await message.answer_photo(
        photo=book.cover,
        caption=caption,
        reply_markup=edit_book_keyboard(l10n, id_book=id_book),
    )
    await state.clear()
