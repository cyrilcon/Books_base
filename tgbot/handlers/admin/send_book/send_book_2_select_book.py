from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import (
    cancel_keyboard,
)
from tgbot.services import (
    ClearKeyboard,
    Messenger,
    generate_book_caption,
    is_book_article,
)
from tgbot.states import SendBook

send_book_router_2 = Router()
send_book_router_2.message.filter(AdminFilter())


@send_book_router_2.callback_query(StateFilter(SendBook.select_book), F.data == "back")
async def back_to_send_book_1(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("send-book-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(SendBook.select_user)


@send_book_router_2.message(StateFilter(SendBook.select_book), F.text)
async def send_book_2(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    await ClearKeyboard.clear(message, storage)

    article = message.text

    if is_book_article(article):
        id_book = int(article.lstrip("#"))

        response = await api.books.get_book_by_id(id_book)
        status = response.status

        if status == 200:
            book = response.result

            data = await state.get_data()
            id_user_recipient = data.get("id_user_recipient")

            caption = await generate_book_caption(data=book, l10n=l10n)

            is_sent = await Messenger.safe_send_message(
                bot=bot,
                user_id=id_user_recipient,
                text=caption,
                photo=book["cover"],
                # reply_markup=deep_link_buy_keyboard(deep_link),  # TODO: добавить кнопку "Купить"
            )

            if is_sent:
                await message.answer(
                    l10n.format_value(
                        "send-book-success",
                        {"title": book["title"]},
                    )
                )
            else:
                await message.answer(l10n.format_value("user-blocked-bot"))
            await state.clear()

        else:
            sent_message = await message.answer(
                l10n.format_value("article-not-found"),
                reply_markup=cancel_keyboard(l10n),
            )
            await ClearKeyboard.safe_message(
                storage=storage,
                user_id=message.from_user.id,
                sent_message_id=sent_message.message_id,
            )
    else:
        sent_message = await message.answer(
            l10n.format_value("article-incorrect"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            user_id=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
