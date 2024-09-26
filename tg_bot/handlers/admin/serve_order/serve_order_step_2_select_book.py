from aiogram import Router, F, Bot
from aiogram.exceptions import AiogramError
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.keyboards.inline import cancel_keyboard, buy_or_read_keyboard
from tg_bot.services import (
    ClearKeyboard,
    get_user_localization,
    generate_book_caption,
    is_valid_book_article,
)
from tg_bot.states import ServeOrder

serve_step_2_router = Router()


@serve_step_2_router.callback_query(
    StateFilter(ServeOrder.select_book), F.data == "back"
)
async def back_to_serve_order_step_1(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_text(
        l10n.format_value("serve-order-prompt-select-order"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(ServeOrder.select_order)
    await call.answer()


@serve_step_2_router.message(StateFilter(ServeOrder.select_book), F.text)
async def serve_step_2(
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
            l10n.format_value("serve-order-error-invalid-article"),
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
            l10n.format_value("serve-order-error-article-not-found"),
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
    id_order = data.get("id_order")

    response = await api.orders.get_order_by_id(id_order)
    order = response.get_model()

    id_user_recipient = order.id_user
    l10n_recipient = await get_user_localization(id_user_recipient)
    caption = await generate_book_caption(book_data=book, l10n=l10n_recipient)

    try:
        sent_message = await bot.send_message(
            chat_id=id_user_recipient,
            text=l10n_recipient.format_value(
                "serve-order-served",
                {"id_order": str(id_order)},
            ),
        )
        await bot.send_photo(
            chat_id=id_user_recipient,
            photo=book.cover,
            caption=caption,
            reply_markup=await buy_or_read_keyboard(
                l10n=l10n,
                id_book=id_book,
                id_user=message.from_user.id,
            ),
            reply_to_message_id=sent_message.message_id,
        )
    except AiogramError:
        await message.answer(l10n.format_value("error-user-blocked-bot"))
    else:
        await message.answer(
            l10n.format_value(
                "serve-order-success",
                {"id_order": str(id_order)},
            )
        )
    await api.orders.delete_order(id_order)
    await state.clear()
