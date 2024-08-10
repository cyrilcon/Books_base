from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from infrastructure.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import cancel_keyboard, edit_book_keyboard
from tgbot.services import (
    ClearKeyboard,
    is_book_article,
    generate_book_caption,
    Messenger,
)
from tgbot.states import EditBook

edit_book_router = Router()
edit_book_router.message.filter(AdminFilter())


@edit_book_router.message(Command("edit_book"))
async def edit_book(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("edit-book-select"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(EditBook.select_book)

    await ClearKeyboard.safe_message(
        storage=storage,
        user_id=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@edit_book_router.message(StateFilter(EditBook.select_book))
async def edit_book_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    await ClearKeyboard.clear(message, storage)

    article = message.text

    if is_book_article(article):
        id_book = int(article[1:])

        response = await api.books.get_book_by_id(id_book)
        status = response.status
        book = response.result

        if status == 200:
            caption = await generate_book_caption(data=book, l10n=l10n)

            await Messenger.safe_send_message(
                bot=bot,
                user_id=message.from_user.id,
                text=caption,
                photo=book["cover"],
                reply_markup=edit_book_keyboard(l10n, id_book),
            )
            await state.clear()
        else:
            await message.answer(
                l10n.format_value("article-not-found"),
                reply_markup=cancel_keyboard(l10n),
            )
    else:
        await message.answer(
            l10n.format_value("article-incorrect"),
            reply_markup=cancel_keyboard(l10n),
        )
