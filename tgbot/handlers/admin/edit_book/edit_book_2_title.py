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
    yes_cancel_keyboard,
    edit_book_keyboard,
)
from tgbot.services import ClearKeyboard, generate_book_caption, Messenger
from tgbot.states import EditBook

edit_book_router_2 = Router()
edit_book_router_2.message.filter(AdminFilter())


@edit_book_router_2.callback_query(F.data.startswith("edit_title"))
async def edit_title(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await call.answer(cache_time=1)

    id_book = int(call.data.split(":")[-1])
    response = await api.books.get_book_by_id(id_book)
    book = response.result

    sent_message = await call.message.answer(
        l10n.format_value("edit-book-title", {"title": book["title"]}),
        reply_markup=cancel_keyboard(l10n),
    )

    await state.update_data(id_book_edited=id_book)
    await state.set_state(EditBook.edit_title)

    await ClearKeyboard.safe_message(
        storage=storage,
        user_id=call.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@edit_book_router_2.message(StateFilter(EditBook.edit_title), F.text)
async def edit_title_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    await ClearKeyboard.clear(message, storage)

    title = message.text

    if len(title) <= 255:
        if '"' in title:
            await message.answer(
                l10n.format_value("add-book-title-incorrect"),
                reply_markup=cancel_keyboard(l10n),
            )
        else:
            await state.update_data(title=title)

            response = await api.books.search_books_by_title(
                title, similarity_threshold=100
            )
            result = response.result
            found = result["found"]

            if found > 0:
                book = result["books"][0]["book"]
                sent_message = await message.answer(
                    l10n.format_value(
                        "title-already-exists",
                        {
                            "title": book["title"],
                            "article": "#{:04d}".format(book["id_book"] + 1),
                        },
                    ),
                    reply_markup=yes_cancel_keyboard(l10n),
                )
                await ClearKeyboard.safe_message(
                    storage=storage,
                    user_id=message.from_user.id,
                    sent_message_id=sent_message.message_id,
                )
            else:
                # TODO: объединить
                data = await state.get_data()
                id_book_edited = data.get("id_book_edited")

                response = await api.books.update_book(id_book_edited, title=title)
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
    else:
        await message.answer(
            l10n.format_value("title-too-long"),
            reply_markup=cancel_keyboard(l10n),
        )


@edit_book_router_2.callback_query(StateFilter(EditBook.edit_title), F.data == "yes")
async def yes_edit_title(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    await call.answer(cache_time=1)

    data = await state.get_data()
    id_book_edited = data.get("id_book_edited")
    title = data.get("title")

    response = await api.books.update_book(id_book_edited, title=title)
    book = response.result

    caption = await generate_book_caption(data=book, l10n=l10n)
    caption_length = len(caption)

    if caption_length <= 1024:
        await call.message.edit_text(l10n.format_value("edit-book-success"))
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
