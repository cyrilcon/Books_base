from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from infrastructure.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import (
    cancel_keyboard,
    edit_book_keyboard,
)
from tgbot.services import ClearKeyboard, generate_book_caption, Messenger
from tgbot.states import EditBook

edit_book_router_3 = Router()
edit_book_router_3.message.filter(AdminFilter())


@edit_book_router_3.callback_query(F.data.startswith("edit_authors"))
async def edit_authors(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await call.answer(cache_time=1)

    id_book = int(call.data.split(":")[-1])
    response = await api.books.get_book_by_id(id_book)
    book = response.result

    authors = ", ".join([author["author"].title() for author in book["authors"]])

    sent_message = await call.message.answer(
        l10n.format_value(
            "edit-book-authors",
            {"authors": f"<code>{authors}</code>"},
        ),
        reply_markup=cancel_keyboard(l10n),
    )

    await state.update_data(id_edit_book=id_book)
    await state.set_state(EditBook.edit_authors)

    await ClearKeyboard.safe_message(
        storage=storage,
        user_id=call.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@edit_book_router_3.message(StateFilter(EditBook.edit_authors), F.text)
async def edit_authors_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    await ClearKeyboard.clear(message, storage)

    authors = message.text.lower().split(", ")

    for author in authors:
        if len(author) > 255:
            sent_message = await message.answer(
                l10n.format_value("authors-too-long"),
                reply_markup=cancel_keyboard(l10n),
            )
            await ClearKeyboard.safe_message(
                storage=storage,
                user_id=message.from_user.id,
                sent_message_id=sent_message.message_id,
            )
            return

    authors = [{"author": author} for author in authors]

    data = await state.get_data()
    id_book_edited = data.get("id_edit_book")

    response = await api.books.update_book(id_book_edited, authors=authors)
    book = response.result

    caption = await generate_book_caption(data=book, l10n=l10n)
    caption_length = len(caption)

    if caption_length <= 1024:
        await message.answer(l10n.format_value("edit-book-success"))
        await Messenger.safe_send_message(
            bot=bot,
            user_id=message.from_user.id,
            text=caption,
            photo=book["cover"],
            reply_markup=edit_book_keyboard(l10n, book["id_book"]),
        )
        await state.clear()
    else:
        sent_message = await message.answer(
            l10n.format_value(
                "edit-book-caption-too-long",
                {"caption_length": caption_length},
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            user_id=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
