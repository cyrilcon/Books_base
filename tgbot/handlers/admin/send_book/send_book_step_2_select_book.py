from aiogram import Router, F, Bot
from aiogram.exceptions import AiogramError
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.keyboards.inline import cancel_keyboard
from tgbot.services import (
    ClearKeyboard,
    generate_book_caption,
    is_valid_book_article,
    get_user_localization,
)
from tgbot.states import SendBook

send_book_step_2_router = Router()


@send_book_step_2_router.callback_query(
    StateFilter(SendBook.select_book), F.data == "back"
)
async def back_to_send_book_step_1(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_text(
        l10n.format_value("send-book-prompt-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(SendBook.select_user)
    await call.answer()


@send_book_step_2_router.message(StateFilter(SendBook.select_book), F.text)
async def send_book_step_2(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    await ClearKeyboard.clear(message, storage)

    article = message.text

    if not is_valid_book_article(article):
        sent_message = await message.answer(
            l10n.format_value("send-book-error-invalid-article"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    id_book = int(article.lstrip("#"))

    response = await api.books.get_book_by_id(id_book)
    status = response.status

    if status != 200:
        sent_message = await message.answer(
            l10n.format_value("send-book-error-article-not-found"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    book = response.get_model()

    data = await state.get_data()
    id_user_recipient = data.get("id_user_recipient")
    user_link = data.get("user_link")

    l10n_recipient = await get_user_localization(id_user_recipient)
    caption = await generate_book_caption(book_data=book, l10n=l10n_recipient)

    try:
        await bot.send_photo(
            chat_id=id_user_recipient,
            photo=book.cover,
            caption=caption,
            # reply_markup=deep_link_buy_keyboard(deep_link),  # TODO: добавить кнопку "Купить"
        )
    except AiogramError:
        await message.answer(l10n.format_value("error-user-blocked-bot"))
    else:
        await message.answer(
            l10n.format_value(
                "send-book-success",
                {
                    "book_title": book.title,
                    "user_link": user_link,
                    "id_user": str(id_user_recipient),
                },
            )
        )
    await state.clear()
