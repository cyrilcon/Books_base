from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import cancel_keyboard, edit_book_keyboard
from tgbot.services import (
    ClearKeyboard,
    is_book_article,
    generate_book_caption,
    Messenger,
)
from tgbot.states import EditBook

edit_book_router_1 = Router()
edit_book_router_1.message.filter(AdminFilter())


@edit_book_router_1.callback_query(F.data.startswith("edit_article"))
async def edit_article(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await call.answer(cache_time=1)

    id_book = int(call.data.split(":")[-1])
    article = "#{:04d}".format(id_book)

    sent_message = await call.message.answer(
        l10n.format_value("edit-book-article", {"article": article}),
        reply_markup=cancel_keyboard(l10n),
    )

    await state.update_data(id_book_edited=id_book)
    await state.set_state(EditBook.edit_article)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=call.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@edit_book_router_1.message(StateFilter(EditBook.edit_article), F.text)
async def edit_article_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    await ClearKeyboard.clear(message, storage)

    article = message.text

    if is_book_article(article):
        new_id_book = int(article[1:])

        response = await api.books.get_book_by_id(new_id_book)
        status = response.status

        if status == 200:
            await message.answer(
                l10n.format_value("article-already-exists"),
                reply_markup=cancel_keyboard(l10n),
            )
        else:
            data = await state.get_data()
            id_book_edited = data.get("id_book_edited")

            response = await api.books.update_book(id_book_edited, id_book=new_id_book)
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
                    id_user=message.from_user.id,
                    sent_message_id=sent_message.message_id,
                )
    else:
        sent_message = await message.answer(
            l10n.format_value("article-incorrect"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
